# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greeting_or_farewell import GreetingOrFarewell


# Definitions

class GreetingJoined(GreetingOrFarewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            message="Welcome, {joiner}!"
        )

    def greet_joined(
        self,
        group_jid: str,
        joined: str | None = None,
    ) -> None:
        super().greet_or_farewell(
            group_jid,
            joined=joined
        )
