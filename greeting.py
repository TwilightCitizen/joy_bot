# Definitions

class Greeting:
    def __init__(self, greeting: str):
        self.enabled = True
        self._greeting: str = greeting

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def set_greeting(self, greeting: str) -> None:
        self._greeting = greeting

    def greet(self) -> str:
        return self._greeting
