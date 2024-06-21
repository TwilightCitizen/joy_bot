# Library Imports

from kik_unofficial.client import KikClient


# Definitions

class Farewell():
    def __init__(
        self,
        farewell: str,
        kik_client: KikClient
    ):
        self.enabled = True
        self._farewell: str = farewell
        self._kik_client: KikClient = kik_client

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def set_greeting(self, farewell: str) -> None:
        self._farewell = farewell

    def farewell(
        self,
        group_jid: str,
        left: str | None = None,
        kicked: str | None = None,
        banned: str | None = None,
        admin: str | None = None,
    ) -> None:
        self._kik_client.send_chat_message(
            group_jid,
            self._farewell.format(
                left=left,
                kicked=kicked,
                banned=banned,
                admin=admin
            )
        )