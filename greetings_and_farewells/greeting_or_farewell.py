# Library Imports

from kik_unofficial.client import KikClient


# Definitions

class GreetingOrFarewell:
    def __init__(
        self,
        message: str,
        kik_client: KikClient
    ):
        self.enabled = True
        self._message: str = message
        self._kik_client: KikClient = kik_client

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def set_greeting(self, greeting: str) -> None:
        self._message = greeting

    def greet_or_farewell(
        self,
        group_jid: str,
        joined: str | None = None,
        invited: str | None = None,
        inviter: str | None = None,
        added: str | None = None,
        adder: str | None = None,
        left: str | None = None,
        kicked: str | None = None,
        banned: str | None = None,
        admin: str | None = None
    ) -> None:
        self._kik_client.send_chat_message(
            group_jid,
            self._message.format(
                joined=joined,
                invited=invited,
                inviter=inviter,
                added=added,
                adder=adder,
                left=left,
                kicked=kicked,
                banned=banned,
                admin=admin
            )
        )