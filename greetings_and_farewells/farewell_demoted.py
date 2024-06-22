# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell


# Definitions

class FarewellDemoted(GreetingOrFarewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            message="Aw...  Sorry, {demoted}, but it's {owners}'s group!"
        )

    def farewell_demoted(
        self,
        group_jid: str,
        demoted: str | None = None,
        owner: str | None = None
    ) -> None:
        super().greet_or_farewell(
            group_jid,
            demoted=demoted,
            owner=owner
        )
