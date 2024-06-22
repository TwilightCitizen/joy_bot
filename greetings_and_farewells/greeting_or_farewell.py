# Library Imports

from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus


# Definitions

class GreetingOrFarewell:
    def __init__(self, kik_client: KikClient, message: str, log_line: str | None = None):
        self.enabled = True
        self._message: str = message
        self._kik_client: KikClient = kik_client
        self._log_line: str | None = log_line

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def set_greeting(self, greeting: str) -> None:
        self._message = greeting

    def greet_or_farewell(self, response: IncomingGroupStatus, **kwargs) -> bool:
        if self._log_line is not None:
            print(self._log_line)

        self._kik_client.send_chat_message(peer_jid=response.group_jid, message=self._message.format(kwargs))

        return True
