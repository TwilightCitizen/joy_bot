# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from farewell import Farewell


# Definitions

class FarewellBanned(Farewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            farewell="Farewell, {banned}.  Thanks, {admin}!"
        )

    def farewell_left(
        self,
        group_jid: str,
        banned: str | None = None,
        admin: str | None = None
    ) -> None:
        super().farewell(
            group_jid,
            banned=banned,
            admin=admin
        )