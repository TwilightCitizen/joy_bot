# Library Imports

from kik_unofficial.client import KikClient

from apscheduler.schedulers.background import BackgroundScheduler

# Application Imports

from utilities_and_helpers.int_range import IntRange


# Definitions

class KeepAlivePing:
    def __init__(self, kik_client: KikClient, background_scheduler: BackgroundScheduler):
        self.interval: IntRange = IntRange(bottom=1, top=30, default=10)
        self.id: str = "KEEP_ALIVE_PING"
        self.kik_client: KikClient = kik_client
        self.background_scheduler: BackgroundScheduler = background_scheduler

    def _send_keep_alive_ping(self):
        self.kik_client.send_ping()
        print("Sent Ping")

    def start(self) -> None:
        if self.background_scheduler.get_job(self.id):
            return

        print("Starting Keep Alive Ping")

        self.background_scheduler.add_job(
            func=self._send_keep_alive_ping,
            trigger="interval",
            minutes=self.interval.get(),
            id=self.id,
        )

    def stop(self) -> None:
        if not self.background_scheduler.get_job(job_id=self.id): return

        print("Stopping Keep Alive Ping")
        self.background_scheduler.remove_job(job_id=self.id)
