# Library Imports

from kik_unofficial.datatypes.peers import User as KikUser
from kik_unofficial.datatypes.peers import GroupMember as KikMember


# Definitions

class User:
    def __init__(self, kik_member: KikMember) -> None:
        # self.public_jid: str = kik_user.jid
        # self.private_jid: str = kik_user.jid
        # self.username: str | None = kik_user.username
        # self.display_name: str = kik_user.display_name
        # self.profile_pic = kik_user.profile_pic
        # self.created_date_seconds = kik_user.creation_date_seconds

        self._public_jid: str = kik_member.jid
        self.is_admin: bool = kik_member.is_admin