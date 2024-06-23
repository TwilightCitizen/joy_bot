# Library Imports

from datetime import datetime, timedelta

from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.peers import User as KikUser

from apscheduler.schedulers.background import BackgroundScheduler


# Definitions

class RequireProfilePics:
    def __init__(self, kik_client: KikClient, background_scheduler: BackgroundScheduler, group_jid: str) -> None:
        self.enabled = True
        self._kik_client = kik_client
        self._background_scheduler = background_scheduler
        self._group_jid = group_jid

        self.message: str = (
            "{joined}, you are being removed because you have no profile picture.  "
            "Come back after you have a profile picture set."
        )

    def check_new_user(self, new_user: KikUser) -> bool:
        if not self.enabled or new_user.profile_pic is not None: return False

        print("User Has No Profile Picture")

        self._kik_client.send_chat_message(
            self._group_jid,
            self.message.format(joined=new_user.display_name)
        )

        self._background_scheduler.add_job(
            func=self._kik_client.remove_peer_from_group,
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=5),
            args=[self._group_jid, new_user.jid],
        )

        return True
