class MiddlewareException(Exception):
    status_code = 400
    def __init__(self, message, code=422) -> None:
        super().__init__(message)

        self.message = message
        self.code = code
