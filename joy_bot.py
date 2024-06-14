import os
import time
import threading

from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.chatting import KikPongResponse
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse, TempBanElement
from kik_unofficial.datatypes.xmpp.roster import PeersInfoResponse
from kik_unofficial.datatypes.xmpp.xiphias import GroupSearchResponse

from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv

load_dotenv()


class JoyBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(
            self,
            os.getenv("JOY_BOT_USERNAME"),
            os.getenv("JOY_BOT_PASSWORD"),
            enable_console_logging=True
        )

        self.user_groups = dict()
        self.scheduler = BackgroundScheduler()

        self.scheduler.start()
        self.client.wait_for_messages()

    def start_keep_alive(self):
        print("Scheduling Periodic Ping for Keep Alive")

        self.scheduler.add_job(
            self.client.send_ping,
            "interval",
            minutes=int(os.getenv("KEEP_ALIVE_PING_INTERVAL_MINUTES_DEFAULT")),
            id="KEEP_ALIVE_INTERVAL"
        )

    def stop_keep_alive(self):
        print("Stopping Periodic Ping for Keep Alive")

        if self.scheduler.get_job("KEEP_ALIVE_INTERVAL"):
            self.scheduler.remove_job("KEEP_ALIVE_INTERVAL")

    def on_authenticated(self):
        print("Authenticated")
        self.start_keep_alive()

    def on_pong(self, response: KikPongResponse):
        print("Received Pong")

    # def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
    #     self.client.send_chat_message(chat_message.from_jid, f'"{chat_message.from_jid}" said "{chat_message.body}"!')

    def on_login_error(self, login_error: LoginError):
        print("Login Error")

        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

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
        self.stop_keep_alive()

    def on_group_status_received(self, response: chatting.IncomingGroupStatus):
        print("Group Status Received")
        print(response.raw_element)

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

    def on_user_joined_group(self, response: chatting.IncomingGroupStatus):
        print("User Joined")
        # print(os.getenv("DEFAULT_JOIN_MESSAGE").format(joiner=response.status_jid))
        self.on_new_user_in_group(response)

    def on_user_invited_to_group(self, response: chatting.IncomingGroupStatus):
        print("User Invited")
        # print(os.getenv("DEFAULT_INVITE_MESSAGE").format(joiner=response.status_jid))
        self.on_new_user_in_group(response)

    def on_user_added_to_group(self, response: chatting.IncomingGroupStatus):
        print("User Added")
        # print(os.getenv("DEFAULT_ADD_MESSAGE").format(joiner=response.status_jid))
        self.on_new_user_in_group(response)

    def on_user_removed_from_group(self, response: chatting.IncomingGroupStatus):
        print("User Removed")
        self.on_user_gone_from_group(response)

    def on_user_left_group(self, response: chatting.IncomingGroupStatus):
        print("User Left")
        self.on_user_gone_from_group(response)

    def on_new_user_in_group(self, response: chatting.IncomingGroupStatus):
        if response.status_jid in self.user_groups.keys():
            self.user_groups[response.status_jid].append(response.group_jid)
        else:
            self.user_groups[response.status_jid] = [response.group_jid]

        self.client.request_info_of_users(response.status_jid)

    def on_user_gone_from_group(self, response: chatting.IncomingGroupStatus):
        print("User Gone")

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("Peer Info Received")
        print(response.raw_element)

        if os.getenv("REQUIRE_PROFILE_PICTURE_ENFORCED"):
            self.on_check_new_user_profile_pic(response)

    def on_check_new_user_profile_pic(self, response: PeersInfoResponse):
        user = response.users[0]

        if user.profile_pic is None and user.jid in self.user_groups.keys():
            user_groups = self.user_groups.pop(user.jid)

            for group in user_groups:
                self.client.send_chat_message(
                    group,
                    os.getenv("REQUIRE_PROFILE_PICTURE_MESSAGE_DEFAULT").format(joiner=user.display_name)
                )

                self.client.remove_peer_from_group(group, user.jid)
        # else:
            # Greet

    def on_group_sysmsg_received(self, response: chatting.IncomingGroupSysmsg):
        print("Group System Message Received")
        print(response.sysmsg)


if __name__ == '__main__':
    _ = JoyBot()
