# Library Imports

import os

from dotenv import load_dotenv

# Definitions


class Authentication:
    def __init__(self):
        load_dotenv()

        self.username: str = "joy_bot_" + os.getenv("BOT_SERIAL")
        self.password: str = os.getenv("BOT_PASSWORD")
        self.email: str = os.getenv("BOT_EMAIl")
