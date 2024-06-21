# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from farewell import Farewell


# Definitions

class FarewellKicked(Farewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            farewell="Farewell, {kicked}.  Thanks, {admin}!"
        )

    def farewell_left(
        self,
        group_jid: str,
        kicked: str | None = None,
        admin: str | None = None
    ) -> None:
        super().farewell(
            group_jid,
            kicked=kicked,
            admin=admin
        )