# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

DEMOTED = " has removed admin status from "


# Definitions

class FarewellDemoted(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Aw...  Sorry, {demoted}, but it's {owner}'s group!",
            log_line="{demoted} Demoted by {owner}"
        )

    @staticmethod
    def can_dispatch(response: IncomingGroupStatus):
        return DEMOTED in response.status

    def farewell_demoted(self, response: IncomingGroupStatus) -> None:
        owner, demoted = response.status.split(DEMOTED)

        super().greet_or_farewell(response=response, demoted=demoted, owner=owner)
