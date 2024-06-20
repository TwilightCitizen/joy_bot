# Library Imports

from kik_unofficial.client import KikClient

from apscheduler.schedulers.background import BackgroundScheduler

# Application Imports

from int_range import IntRange


# Definitions


class KeepAlivePing:
    def __init__(self, kik_client: KikClient, background_scheduler: BackgroundScheduler):
        self.interval: IntRange = IntRange(bottom=1, top=30, default=10)
        self.enabled: bool = True
        self.id: str = "KEEP_ALIVE_PING"
        self.kik_client: KikClient = kik_client
        self.background_scheduler: BackgroundScheduler = background_scheduler

    def start(self) -> None:
        if not self.enabled:
            return

        print("Starting Keep Alive Ping")

        self.background_scheduler.add_job(
            self.kik_client.send_ping,
            "interval",
            minutes=int(self.interval.get()),
            id=self.id,
        )

    def stop(self) -> None:
        if not self.enabled:
            return

        print("Stopping Keep Alive Ping")

        if self.background_scheduler.get_job(self.id):
            self.background_scheduler.remove_job(self.id)