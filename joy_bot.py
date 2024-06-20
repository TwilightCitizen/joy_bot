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
from limit_member_capacity import LimitMemberCapacity
from disallow_quiet_joiners import DisallowQuietJoiners
from disallow_quiet_lurkers import DisallowQuietLurkers
from require_profile_pics import RequireProfilePics
from require_minimum_account_age import RequireMinimumAccountAge

# Configuration

load_dotenv()

# Definitions


class JoyBot(KikClientCallback):
    def __init__(self):
        print("Initializing")

        self.authentication: Authentication = Authentication()
        self.limit_member_capacity: LimitMemberCapacity = LimitMemberCapacity()
        self.disallow_quiet_joiners: DisallowQuietJoiners = DisallowQuietJoiners()
        self.disallow_quiet_lurkers: DisallowQuietLurkers = DisallowQuietLurkers()
        self.require_profile_pics: RequireProfilePics = RequireProfilePics()
        self.require_min_account_age: RequireMinimumAccountAge = RequireMinimumAccountAge()
        self.background_scheduler: BackgroundScheduler = BackgroundScheduler()
        self.users_groups: dict[str, list[str]] = dict()

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

        self.kik_client.wait_for_messages()
        self.background_scheduler.start()

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
        print("Group Status Received")
        print(response.raw_element.prettify())

        if "has joined the chat" in response.status:
            self.on_user_joined_group(response)
        elif "has been invited to the group by" in response.status:
            self.on_user_invited_to_group(response)
        elif "was added to the group by" in response.status:
            self.on_user_added_to_group(response)
        elif "has left the chat" in response.status:
            self.on_user_left_group(response)
        elif "have removed" in response.status or "has removed" in response.status:
            self.on_user_removed_from_group(response)
        elif "has promoted" in response.status:
            self.on_user_promoted_in_group(response)

    def on_user_joined_group(self, response: IncomingGroupStatus):
        print("User Joined")
        self.on_new_user_in_group(response)

    def on_user_invited_to_group(self, response: IncomingGroupStatus):
        print("User Invited")
        self.on_new_user_in_group(response)

    def on_user_added_to_group(self, response: IncomingGroupStatus):
        print("User Added")
        self.on_new_user_in_group(response)

    def on_user_removed_from_group(self, response: IncomingGroupStatus):
        print("User Removed")
        self.on_user_gone_from_group(response)

    def on_user_left_group(self, response: IncomingGroupStatus):
        print("User Left")
        self.on_user_gone_from_group(response)

    def on_new_user_in_group(self, response: IncomingGroupStatus):
        print("New User")

        if response.status_jid in self.users_groups.keys():
            self.users_groups[response.status_jid].append(response.group_jid)
        else:
            self.users_groups[response.status_jid] = [response.group_jid]

        self.kik_client.request_info_of_users(response.status_jid)
        self.kik_client.xiphias_get_users(response.status_jid)

    def on_user_gone_from_group(self, response: IncomingGroupStatus):
        print("User Gone")

    def on_user_promoted_in_group(self, response: IncomingGroupStatus):
        print("User Promoted")

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

                print(self.background_scheduler.get_jobs())

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
