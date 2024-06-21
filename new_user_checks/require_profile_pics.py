# Definitions

class RequireProfilePics:
    def __init__(self):
        self.enabled = True

        self.message: str = (
            "{joiner}, you are being removed because you have no profile picture.  "
            "Come back after you have a profile picture set."
        )
