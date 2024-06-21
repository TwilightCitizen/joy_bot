# Library Imports

from typing import Callable

from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupStatus

# Application Imports

from joy_bot import JoyBot

# Constants

JOINED = " has joined the chat"
INVITED = " has been invited to the group by "
ADDED = " was added to the group by "

LEFT = " has left the chat"
KICKED1 = " has removed "
KICKED2 = " from this group"
BANNED = " has banned "
UNBANNED = " has unbanned "

PROMOTED1 = " has promoted "
PROMOTED2 = " to admin"
DEMOTED = " has removed admin status from "

# Definitions

class GreeterAndFareweller:
    def __init__(
        self,
        joy_bot: JoyBot,
        after
    ):
        self.joy_bot = joy_bot

    def dispatch_greeting_or_farewell(self, response: IncomingGroupStatus) -> None:
        message = response.status

        if JOINED in message:
            print("User Joined")

            joined = message.split(JOINED)
            greeting = self.joy_bot.greeting_joined

            if greeting.enabled:
                greeting.greet_or_farewell(joined=joined)

        elif INVITED in message:
            print("User Invited")

            invited, inviter = message.split(INVITED)
            greeting = self.joy_bot.greeting_invited

            if greeting.enabled:
                greeting.greet_or_farewell(invited=invited, inviter=inviter)

        elif ADDED in message:
            print("User Added")

            added, adder = message.split(ADDED)
            greeting = self.joy_bot.greeting_invited

            if greeting.enabled:
                greeting.greet_or_farewell(added=added,  adder=adder)

        if LEFT in message:
            print("User Left")

            left = message.split(LEFT)
            farewell = self.joy_bot.farewell_left

            if farewell.enabled:
                farewell.greet_or_farewell(left=left)

        elif KICKED1 in message and KICKED2 in message:
            print("User Kicked")

            admin, rest = message.split(KICKED1)
            kicked = rest.split(KICKED2)
            farewell = self.joy_bot.farewell_kicked

            if farewell.enabled:
                farewell.greet_or_farewell(kicked=kicked, admin=admin)

        elif PROMOTED1 in message and PROMOTED2 in message:
            return

        elif DEMOTED in message:
            return
