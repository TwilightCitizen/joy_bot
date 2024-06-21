# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greeting_or_farewell import GreetingOrFarewell


# Definitions

class GreetingInvited(GreetingOrFarewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            message="Welcome, {invited}, invited by {inviter}!"
        )

    def greet_invited(
        self,
        group_jid: str,
        invited: str | None = None,
        inviter: str | None = None,
    ) -> None:
        super().greet_or_farewell(
            group_jid,
            invited=invited,
            inviter=inviter,
        )
