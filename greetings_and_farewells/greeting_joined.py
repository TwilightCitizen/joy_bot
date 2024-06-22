# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

JOINED = " has joined the chat"


# Definitions

class GreetingJoined(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Welcome, {joined}!",
            log_line="{joined} Joined"
        )

    @staticmethod
    def can_dispatch(response: IncomingGroupStatus):
        return JOINED in response.status

    def greet_joined(self, response: IncomingGroupStatus) -> None:
        joined, _ = response.status.split(JOINED)

        super().greet_or_farewell(response=response, joined=joined)
