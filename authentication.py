# Library Imports

import os

from dotenv import load_dotenv

# Configuration

load_dotenv()

# Definitions


class Authentication:
    def __init__(self):
        self.username: str = "joy_bot_" + os.getenv("BOT_SERIAL")
        self.password: str = os.getenv("BOT_PASSWORD")
        self.email: str = os.getenv("BOT_EMAIl")