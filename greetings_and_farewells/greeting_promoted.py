# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell


# Definitions

class GreetingPromoted(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(kik_client=kik_client, message="Congrats, {promoted}...  {admin} must like you!")

    def greet_promoted(self, group_jid: str, promoted: str | None = None, admin: str | None = None) -> None:
        super().greet_or_farewell(group_jid, promoted=promoted, admin=admin)
