""" Exceptions that happen during posting """


class PostSendException(Exception):
    """ Raised when sending a post fails """

    def __init__(self, message: str, allow_retry: bool):
        """
        :param message: A human readable error message
        :param allow_retry: True if post should be attempted again
        """
        super().__init__(message)
        self.message = message
        self.allow_retry = allow_retry

    def as_dict(self):
        """ Convert to dict """
        return {"message": self.message, "allow_retry": self.allow_retry}
