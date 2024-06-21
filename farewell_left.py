# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from farewell import Farewell


# Definitions

class FarewellLeft(Farewell):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            farewell="Farewell, {left}!"
        )

    def farewell_left(
        self,
        group_jid: str,
        left: str | None = None,
    ) -> None:
        super().farewell(
            group_jid,
            left=left
        )