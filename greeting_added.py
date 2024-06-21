# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greeting import Greeting


# Definitions

class GreetingAdd(Greeting):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            greeting="Welcome, {added}, added by {adder}!"
        )

    def greet_invited(
            self,
            group_jid: str,
            added: str | None = None,
            adder: str | None = None,
    ) -> None:
        super().greet(
            group_jid,
            added=added,
            adder=adder,
        )
