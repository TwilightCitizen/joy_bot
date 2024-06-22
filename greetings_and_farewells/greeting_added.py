# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

ADDED = " was added to the group by "


# Definitions

class GreetingAdded(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Welcome, {added}, added by {adder}!",
            log_line="{added} Added by {adder}"
        )

    def greet_added(self, response: IncomingGroupStatus) -> bool:
        if ADDED not in response.status: return False

        added, adder = response.status.split(ADDED)

        return super().greet_or_farewell(response=response, added=added, adder=adder)
