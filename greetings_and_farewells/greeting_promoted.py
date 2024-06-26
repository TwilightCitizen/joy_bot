# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

PROMOTED1 = " has promoted "
PROMOTED2 = " to admin"


# Definitions

class GreetingPromoted(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Congrats, {promoted}...  {admin} must like you!",
            log_line="{promoted} Promoted by {admin}"
        )

    def greet_or_farewell(self, response: IncomingGroupStatus) -> bool:
        if not (PROMOTED1 in response.status and PROMOTED2 in response.status): return False

        admin, rest = response.status.split(PROMOTED1)
        promoted, _ = rest.split(PROMOTED2)

        return super()._greet_or_farewell(response=response, promoted=promoted, admin=admin)
