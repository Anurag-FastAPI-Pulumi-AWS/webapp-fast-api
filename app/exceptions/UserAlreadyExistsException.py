class UserAlreadyExistsException(Exception):
    def __init__(self, message="User Already Exists!"):
        self.message = message
        super().__init__(self.message)
