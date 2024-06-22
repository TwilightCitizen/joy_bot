# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

KICKED1 = " has removed "
KICKED2 = " from this group"


# Definitions

class FarewellKicked(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient ):
        super().__init__(
            kik_client=kik_client,
            message="Farewell, {kicked}.  Thanks, {admin}!",
            log_line="{kicked} Kicked by {admin}"
        )

    def farewell_kicked(self, response: IncomingGroupStatus) -> bool:
        if not (KICKED1 in response.status and KICKED2 in response.status): return False

        admin, rest = response.status.split(KICKED1)
        kicked, _ = rest.split(KICKED2)

        return super().greet_or_farewell(response=response, kicked=kicked, admin=admin)
