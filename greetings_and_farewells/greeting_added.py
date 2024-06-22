# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell


# Definitions

class GreetingAdded(GreetingOrFarewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            message="Welcome, {added}, added by {adder}!"
        )

    def greet_invited(
            self,
            group_jid: str,
            added: str | None = None,
            adder: str | None = None,
    ) -> None:
        super().greet_or_farewell(
            group_jid,
            added=added,
            adder=adder,
        )
