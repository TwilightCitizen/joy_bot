# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

BANNED = " has banned "


# Definitions

class FarewellBanned(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Farewell, {banned}.  Thanks, {admin}!",
            log_line="{banned} Banned by {admin}"
        )

    def greet_or_farewell(self, response: IncomingGroupStatus, **kwargs) -> bool:
        if BANNED not in response.status: return False

        admin, banned = response.status.split(BANNED)

        return super().greet_or_farewell(response=response, banned=banned, admin=admin)
