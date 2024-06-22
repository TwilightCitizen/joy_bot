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

    @staticmethod
    def can_dispatch(response: IncomingGroupStatus):
        return BANNED in response.status

    def farewell_banned(self, response: IncomingGroupStatus) -> None:
        admin, banned = response.status.split(BANNED)

        super().greet_or_farewell(response=response, banned=banned, admin=admin)
