# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell


# Definitions

class FarewellBanned(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(kik_client=kik_client, message="Farewell, {banned}.  Thanks, {admin}!")

    def farewell_left(self, group_jid: str, banned: str | None = None, admin: str | None = None) -> None:
        super().greet_or_farewell(group_jid, banned=banned, admin=admin )
