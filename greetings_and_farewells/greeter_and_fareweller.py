# Library Imports

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
        joy_bot: JoyBot
    ):
        self.joy_bot = joy_bot

    def dispatch_greeting_or_farewell(
        self,
        response: IncomingGroupStatus
    ) -> None:
        message = response.status
        group_jid = response.group_jid

        if JOINED in message:
            joined = message.split(JOINED)
            greeting = self.joy_bot.greeting_joined

            print("{joined} Joined".format(
                joined=joined
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    joined=joined
                )

            self.joy_bot.on_new_user_in_group(response)

        elif INVITED in message:
            invited, inviter = message.split(INVITED)
            greeting = self.joy_bot.greeting_invited

            print("{invited} Invited by {inviter}".format(
                invited=invited,
                inviter=inviter
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    invited=invited,
                    inviter=inviter
                )

            self.joy_bot.on_new_user_in_group(response)

        elif ADDED in message:
            added, adder = message.split(ADDED)
            greeting = self.joy_bot.greeting_invited

            print("{added} Added by {adder}".format(
                added=added,
                adder=adder
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    added=added,
                    adder=adder
                )

            self.joy_bot.on_new_user_in_group(response)

        elif LEFT in message:
            left = message.split(LEFT)
            farewell = self.joy_bot.farewell_left

            print("{left} Left".format(
                left=left
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    left=left
                )

            self.joy_bot.on_new_user_in_group(response)

        elif KICKED1 in message and KICKED2 in message:
            admin, rest = message.split(KICKED1)
            kicked = rest.split(KICKED2)
            farewell = self.joy_bot.farewell_kicked

            print("{kicked} Kicked by {admin}".format(
                kicked=kicked,
                admin=admin
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    kicked=kicked,
                    admin=admin
                )

        elif BANNED in message:
            admin, banned = message.split(BANNED)
            farewell = self.joy_bot.farewell_banned

            print("{banned} Banned by {admin}".format(
                banned=banned,
                admin=admin
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    banned=banned,
                    admin=admin
                )

        elif PROMOTED1 in message and PROMOTED2 in message:
            admin, rest = message.split(PROMOTED1)
            promoted = rest.split(PROMOTED2)
            greeting = self.joy_bot.greeting_promoted

            print("{promoted} Promoted by {admin}".format(
                promoted=promoted,
                admin=admin
            ))

            if greeting.enabled:
                greeting.greet_or_farewell(
                    group_jid,
                    promoted=promoted,
                    admin=admin
                )

        elif DEMOTED in message:
            owner, demoted = message.split(DEMOTED)
            farewell = self.joy_bot.farewell_demoted

            print("{demoted} Demoted by {owner}".format(
                demoted=demoted,
                owner=owner
            ))

            if farewell.enabled:
                farewell.greet_or_farewell(
                    group_jid,
                    demoted=demoted,
                    owner=owner
                )

        else:
            print("Other Incoming Group Status Received")
            print(response.raw_element.prettify())
