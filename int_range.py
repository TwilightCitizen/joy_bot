class IntRange:
    def __init__(self, bottom: int, top: int, default: int):
        if bottom > top:
            raise ValueError("Bottom must be less than or equal to top.")

        if default < bottom or default > top:
            raise ValueError("Default must be between bottom and top.")

        self._bottom: int = bottom
        self._top: int = top
        self._value: int = default

    def get(self) -> int:
        return self._value

    def set(self, value: int):
        if value < self._bottom or value > self._top:
            raise ValueError("Value must be between bottom and top.")

        self._value = value