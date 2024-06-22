# Library Imports

from datetime import datetime, timedelta
from typing import Union

from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import KikPongResponse, IncomingGroupStatus, IncomingGroupSysmsg
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse, TempBanElement
from kik_unofficial.datatypes.xmpp.roster import PeersInfoResponse, FetchRosterResponse
from kik_unofficial.datatypes.xmpp.xiphias import UsersResponse, UsersByAliasResponse
from kik_unofficial.datatypes.peers import User, Group

from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv

# Application Imports

from authentication import Authentication
from keep_alive_ping import KeepAlivePing

from new_user_checks.limit_member_capacity import LimitMemberCapacity
from new_user_checks.disallow_quiet_joiners import DisallowQuietJoiners
from new_user_checks.disallow_quiet_lurkers import DisallowQuietLurkers
from new_user_checks.require_profile_pics import RequireProfilePics
from new_user_checks.require_minimum_account_age import RequireMinimumAccountAge

from greetings_and_farewells.greeting_joined import GreetingJoined
from greetings_and_farewells.greeting_invited import GreetingInvited
from greetings_and_farewells.greeting_added import GreetingAdded
from greetings_and_farewells.greeting_promoted import GreetingPromoted
from greetings_and_farewells.farewell_left import FarewellLeft
from greetings_and_farewells.farewell_kicked import FarewellKicked
from greetings_and_farewells.farewell_banned import FarewellBanned
from greetings_and_farewells.farewell_demoted import FarewellDemoted

# Constants

JOINED = " has joined the chat"
INVITED = " has been invited to the group by "
ADDED = " was added to the group by "

LEFT = " has left the chat"
KICKED1 = " has removed "
KICKED2 = " from this group"
BANNED = " has banned "
UNBANNED = " has unbanned "

PROMOTED1 = " has promoted "
PROMOTED2 = " to admin"
DEMOTED = " has removed admin status from "


# Definitions

class JoyBot(KikClientCallback):
    def __init__(self):
        print("Initializing")
        load_dotenv()

        self.authentication: Authentication = Authentication()

        self.limit_member_capacity: LimitMemberCapacity = LimitMemberCapacity()
        self.disallow_quiet_joiners: DisallowQuietJoiners = DisallowQuietJoiners()
        self.disallow_quiet_lurkers: DisallowQuietLurkers = DisallowQuietLurkers()
        self.require_profile_pics: RequireProfilePics = RequireProfilePics()
        self.require_min_account_age: RequireMinimumAccountAge = RequireMinimumAccountAge()

        self.background_scheduler: BackgroundScheduler = BackgroundScheduler()
        self.users_groups: dict[str, list[str]] = dict()

        print("Starting Background Scheduler")
        self.background_scheduler.start()
        print("Authenticating")

        self.kik_client: KikClient = KikClient(
            self,
            self.authentication.username,
            self.authentication.password,
            enable_console_logging=True
        )

        self.keep_alive_ping: KeepAlivePing = KeepAlivePing(
            kik_client=self.kik_client,
            background_scheduler=self.background_scheduler
        )

        self.greeting_joined: GreetingJoined = GreetingJoined(self.kik_client)
        self.greeting_invited: GreetingInvited = GreetingInvited(self.kik_client)
        self.greeting_added: GreetingAdded = GreetingAdded(self.kik_client)
        self.greeting_promoted: GreetingPromoted = GreetingPromoted(self.kik_client)
        self.farewell_left: FarewellLeft = FarewellLeft(self.kik_client)
        self.farewell_kicked: FarewellKicked = FarewellKicked(self.kik_client)
        self.farewell_banned: FarewellBanned = FarewellBanned(self.kik_client)
        self.farewell_demoted: FarewellDemoted = FarewellDemoted(self.kik_client)

        self.kik_client.wait_for_messages()

    def on_authenticated(self):
        print("Authenticated")
        self.keep_alive_ping.start()
        print("Requesting Rosters")
        self.kik_client.request_roster()

    def on_pong(self, response: KikPongResponse):
        print("Received Pong")

    def on_login_error(self, login_error: LoginError):
        print("Login Error")

        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.kik_client)

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("Connection Failed")
        print(response.message)

        if response.is_backoff:
            print("Backoff Seconds:", response.backoff_seconds)

    def on_temp_ban_received(self, response: TempBanElement):
        print("Temporary Ban Received")
        print(response.ban_title)
        print(response.ban_message)
        print(response.ban_end_time)

    def on_disconnected(self):
        print("Disconnected")
        self.keep_alive_ping.stop()

    def on_group_status_received(self, response: IncomingGroupStatus):
        message = response.status
        group_jid = response.group_jid

        if JOINED in message:
            joined, _ = message.split(JOINED)
            greeting = self.greeting_joined

            print("{joined} Joined".format(
                joined=joined
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    joined=joined
                )

            self.on_new_user_in_group(response)

        elif INVITED in message:
            invited, inviter = message.split(INVITED)
            greeting = self.greeting_invited

            print("{invited} Invited by {inviter}".format(
                invited=invited,
                inviter=inviter
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    invited=invited,
                    inviter=inviter
                )

            self.on_new_user_in_group(response)

        elif ADDED in message:
            added, adder = message.split(ADDED)
            greeting = self.greeting_invited

            print("{added} Added by {adder}".format(
                added=added,
                adder=adder
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    added=added,
                    adder=adder
                )

            self.on_new_user_in_group(response)

        elif LEFT in message:
            left, _ = message.split(LEFT)
            farewell = self.farewell_left

            print("{left} Left".format(
                left=left
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    left=left
                )

        elif KICKED1 in message and KICKED2 in message:
            admin, rest = message.split(KICKED1)
            kicked, _ = rest.split(KICKED2)
            farewell = self.farewell_kicked

            print("{kicked} Kicked by {admin}".format(
                kicked=kicked,
                admin=admin
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    kicked=kicked,
                    admin=admin
                )

        elif BANNED in message:
            admin, banned = message.split(BANNED)
            farewell = self.farewell_banned

            print("{banned} Banned by {admin}".format(
                banned=banned,
                admin=admin
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    banned=banned,
                    admin=admin
                )

        elif PROMOTED1 in message and PROMOTED2 in message:
            admin, rest = message.split(PROMOTED1)
            promoted, _ = rest.split(PROMOTED2)
            greeting = self.greeting_promoted

            print("{promoted} Promoted by {admin}".format(
                promoted=promoted,
                admin=admin
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    promoted=promoted,
                    admin=admin
                )

        elif DEMOTED in message:
            owner, demoted = message.split(DEMOTED)
            farewell = self.farewell_demoted

            print("{demoted} Demoted by {owner}".format(
                demoted=demoted,
                owner=owner
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    demoted=demoted,
                    owner=owner
                )

        else:
            print("Other Incoming Group Status Received")
            print(response.raw_element.prettify())

    def on_new_user_in_group(self, response: IncomingGroupStatus):
        if response.status_jid in self.users_groups.keys():
            self.users_groups[response.status_jid].append(response.group_jid)
        else:
            self.users_groups[response.status_jid] = [response.group_jid]

        self.kik_client.request_info_of_users(response.status_jid)
        self.kik_client.xiphias_get_users(response.status_jid)

    def on_roster_received(self, response: FetchRosterResponse):
        print("Rosters Received")
        print(response.raw_element.prettify())

        groups: list[Group] = [elem for elem in response.peers if isinstance(elem, Group)]

        for group in groups:
            print(group.name)

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("Peer Info Received")
        print(response.raw_element.prettify())

        if self.require_profile_pics.enabled:
            if self.new_user_account_is_missing_profile_pic(response):
                return

    def on_xiphias_get_users_response(self, response: Union[UsersResponse, UsersByAliasResponse]):
        print("Xiphias Info Received")
        print(response.raw_element.prettify())

        if self.require_min_account_age.enabled:
            if self.new_user_account_age_is_less_than_minimum_days(response):
                return

    def new_user_account_is_missing_profile_pic(self, response: PeersInfoResponse):
        user: User = response.users[0]

        if user.profile_pic is None and user.jid in self.users_groups.keys():
            print("User Has No Profile Picture")

            user_groups = self.users_groups.pop(user.jid)

            for group in user_groups:
                self.kik_client.send_chat_message(
                    group,
                    self.require_profile_pics.message.format(joiner=user.display_name)
                )

                self.background_scheduler.add_job(
                    self.kik_client.remove_peer_from_group,
                    "date",
                    run_date=datetime.now() + timedelta(seconds=5),
                    args=[group, user.jid],
                )

                self.background_scheduler.print_jobs()

            return True

        else:
            return False

    def new_user_account_age_is_less_than_minimum_days(self, response: Union[UsersResponse, UsersByAliasResponse]):
        # user = response.users[0]
        # epoch = datetime(1970, 1, 1)
        # epoch_to_now_delta = datetime.now() - epoch
        # epoch_to_now_seconds = epoch_to_now_delta.total_seconds()
        # epoch_plus_creation_date_seconds = epoch + timedelta(seconds=user.creation_date_seconds)
        #
        # print("Account Age in Seconds: ", user.creation_date_seconds)
        # print("Today's Date in Seconds: ", epoch_to_now_seconds)
        # print("User Account Creation Date: ", epoch_plus_creation_date_seconds)

        print(response.message)

        return False

    def on_group_sysmsg_received(self, response: IncomingGroupSysmsg):
        print("Group System Message Received")

        print(response.sysmsg)

# Execution

if __name__ == '__main__':
    _ = JoyBot()
