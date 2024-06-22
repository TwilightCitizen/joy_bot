# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greeting_or_farewell import GreetingOrFarewell


# Definitions

class FarewellKicked(GreetingOrFarewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            message="Farewell, {kicked}.  Thanks, {admin}!"
        )

    def farewell_left(
        self,
        group_jid: str,
        kicked: str | None = None,
        admin: str | None = None
    ) -> None:
        super().greet_or_farewell(
            group_jid,
            kicked=kicked,
            admin=admin
        )
