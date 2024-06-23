# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greetings_and_farewells.greeting_or_farewell import GreetingOrFarewell
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Constants

INVITED = " has been invited to the group by "


# Definitions

class GreetingInvited(GreetingOrFarewell):
    def __init__(self, kik_client: KikClient):
        super().__init__(
            kik_client=kik_client,
            message="Welcome, {invited}, invited by {inviter}!",
            log_line="{invited} Invited by {inviter}"
        )

    def greet_or_farewell(self, response: IncomingGroupStatus) -> bool:
        if INVITED not in response.status: return False

        invited, inviter = response.status.split(INVITED)

        return super()._greet_or_farewell(response=response, invited=invited, inviter=inviter)
