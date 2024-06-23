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
from kik_unofficial.datatypes.peers import User as KikUser, Group as KikGroup

from apscheduler.schedulers.background import BackgroundScheduler

# Application Imports

from authentication import Authentication
from keep_alive_ping import KeepAlivePing

from users_and_groups.group import Group


# Definitions

class JoyBot(KikClientCallback):
    def __init__(self):
        print("Initializing")

        self._authentication: Authentication = Authentication()
        self._background_scheduler: BackgroundScheduler = BackgroundScheduler()

        self.groups: dict[str, Group] = dict()

        print("Starting Background Scheduler")
        self._background_scheduler.start()
        print("Authenticating")

        self._kik_client: KikClient = KikClient(
            callback=self,
            kik_username=self._authentication.username,
            kik_password=self._authentication.password,
            enable_console_logging=True
        )

        self._keep_alive_ping: KeepAlivePing = KeepAlivePing(
            kik_client=self._kik_client,
            background_scheduler=self._background_scheduler
        )

        self._kik_client.wait_for_messages()

    def on_authenticated(self):
        print("Authenticated")
        self._keep_alive_ping.start()
        print("Requesting Rosters")
        self._kik_client.request_roster()

    def on_pong(self, response: KikPongResponse):
        print("Received Pong")

    def on_login_error(self, login_error: LoginError):
        print("Login Error")

        if login_error.is_captcha():
            login_error.solve_captcha_wizard(kik_client=self._kik_client)

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("Connection Failed")
        print(response.message)

        if response.is_backoff: print("Backoff Seconds:", response.backoff_seconds)

    def on_temp_ban_received(self, response: TempBanElement):
        print("Temporary Ban Received")
        print(response.ban_title)
        print(response.ban_message)
        print(response.ban_end_time)

    def on_disconnected(self):
        print("Disconnected")
        self._keep_alive_ping.stop()

    def on_group_status_received(self, response: IncomingGroupStatus):
        group: Group = self.groups[response.group_jid]

        group.dispatch_group_status(response=response)

    def on_roster_received(self, response: FetchRosterResponse):
        print("Rosters Received")

        for elem in response.peers:
            if isinstance(elem, KikGroup):
                kik_group: KikGroup = elem

                self.groups[kik_group.jid] = Group(
                    kik_client=self._kik_client,
                    kik_group=kik_group,
                    background_scheduler=self._background_scheduler
                )

        for group in self.groups.values():
            print(group.__dict__)

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("Peer Info Received")
        print(response.raw_element.prettify())
        print(response.group_jid)

        kik_user: KikUser = response.users[0]

        for group in self.groups.values():
            group.check_new_user(kik_user)

    def on_xiphias_get_users_response(self, response: Union[UsersResponse, UsersByAliasResponse]):
        print("Xiphias Info Received")
        print(response.raw_element.prettify())

    def on_group_sysmsg_received(self, response: IncomingGroupSysmsg):
        print("Group System Message Received")

        print(response.sysmsg)


# Execution

if __name__ == '__main__':
    _ = JoyBot()
