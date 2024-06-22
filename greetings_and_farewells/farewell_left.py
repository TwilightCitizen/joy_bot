# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

LEFT = " has left the chat"


# Definitions

class FarewellLeft(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Farewell, {left}!",
            log_line="{left} Left"
        )

    def farewell_left(self, response: IncomingGroupStatus) -> bool:
        if LEFT not in response.status: return False

        left, _ = response.status.split(LEFT)

        return super().greet_or_farewell(response=response, left=left)
