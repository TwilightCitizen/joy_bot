# Library Imports

from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.peers import Group as KikGroup
from kik_unofficial.datatypes.peers import User as KikUser
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

from apscheduler.schedulers.background import BackgroundScheduler

# Application Imports

from greetings_and_farewells.greeting_joined import GreetingJoined
from greetings_and_farewells.greeting_invited import GreetingInvited
from greetings_and_farewells.greeting_added import GreetingAdded
from greetings_and_farewells.greeting_promoted import GreetingPromoted
from greetings_and_farewells.farewell_left import FarewellLeft
from greetings_and_farewells.farewell_kicked import FarewellKicked
from greetings_and_farewells.farewell_banned import FarewellBanned
from greetings_and_farewells.farewell_demoted import FarewellDemoted
from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell

from new_user_checks.limit_member_capacity import LimitMemberCapacity
from new_user_checks.disallow_quiet_joiners import DisallowQuietJoiners
from new_user_checks.disallow_quiet_lurkers import DisallowQuietLurkers
from new_user_checks.require_profile_pics import RequireProfilePics
from new_user_checks.require_minimum_account_age import RequireMinimumAccountAge


# Definitions

class Group:
    def __init__(self, kik_client: KikClient, background_scheduler: BackgroundScheduler, kik_group: KikGroup):
        self._kik_client = kik_client
        self._background_scheduler = background_scheduler

        self._jid: str = kik_group.jid
        self._hash_tag: str | None = kik_group.code
        self._name: str = kik_group.name
        self._pic: str = kik_group.pic

        self.pending_members: list[str] = []
        self.members: list[str] = []

        for member in kik_group.members:
            self.members.append(member.jid)

        self.greeting_joined: GreetingJoined = GreetingJoined(kik_client=self._kik_client)
        self.greeting_invited: GreetingInvited = GreetingInvited(kik_client=self._kik_client)
        self.greeting_added: GreetingAdded = GreetingAdded(kik_client=self._kik_client)
        self.greeting_promoted: GreetingPromoted = GreetingPromoted(kik_client=self._kik_client)
        self.farewell_left: FarewellLeft = FarewellLeft(kik_client=self._kik_client)
        self.farewell_kicked: FarewellKicked = FarewellKicked(kik_client=self._kik_client)
        self.farewell_banned: FarewellBanned = FarewellBanned(kik_client=self._kik_client)
        self.farewell_demoted: FarewellDemoted = FarewellDemoted(kik_client=self._kik_client)

        # self.limit_member_capacity: LimitMemberCapacity = LimitMemberCapacity()
        # self.disallow_quiet_joiners: DisallowQuietJoiners = DisallowQuietJoiners()
        # self.disallow_quiet_lurkers: DisallowQuietLurkers = DisallowQuietLurkers()

        self.require_profile_pics: RequireProfilePics = RequireProfilePics(
            kik_client=self._kik_client,
            background_scheduler=self._background_scheduler,
            group_jid=self._jid
        )

        # self.require_min_account_age: RequireMinimumAccountAge = RequireMinimumAccountAge()

    @property
    def jid(self):
        return self._jid

    def dispatch_group_status(self, response: IncomingGroupStatus):
        def gof(x: GreetingOrFarewell): return x.greet_or_farewell(response=response)

        if any(map(gof, [self.greeting_joined, self.greeting_invited, self.greeting_added])):
            self.pending_members.append(response.status_jid)
            self._kik_client.request_info_of_users(response.status_jid)
            # self.kik_client.xiphias_get_users(response.status_jid)
        elif not any(map(gof, [
            self.farewell_left, self.farewell_kicked, self.farewell_banned,
            self.greeting_promoted, self.farewell_demoted
        ])):
            print("Other Incoming Group Status Received")
            print(response.raw_element.prettify())

    def check_new_user(self, new_user: KikUser):
        if new_user.jid in self.pending_members:
            if self.require_profile_pics.check_new_user(new_user=new_user):
                self.pending_members.remove(new_user.jid)
            else:
                self.members.append(new_user.jid)
                self.pending_members.remove(new_user.jid)