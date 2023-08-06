"""Exceptions.
"""


class ConnectToServerException(Exception):
    """Raised on a general inability to connect to the server.
    """

    def __init__(self, response, *args, **kwargs):
        """Generate a readable message.
        """
        msg = 'The server encountered an error.\nCode: {}\nMessage: {}'.format(
            response.status_code,
            response.text)
        super().__init__(msg, *args, **kwargs)


class NotSetupException(Exception):
    """Raised when the app hasn't been configured correctly.
    """


class ServerResponseException(Exception):
    """Raised when the server returns 400.
    """

    def __init__(self, response, *args, **kwargs):
        """Generate a readable message.
        """
        content = response.json()
        errors = '\n'.join(': '.join((k, v)) for k, v in content.items())
        msg = 'The server did not like your response: {}'.format(errors)
        super().__init__(msg, *args, **kwargs)


class WrongElvesException(Exception):
    """Raised when the developer has sent the wrong number of elves.
    """

    def __init__(self, woods, forest, mountain, total, *args, **kwargs):
        """Generate a readable message.
        """
        msg = ('Must send {total} elves this turn. You sent:\n'
               '{woods} woods\n'
               '{forest} forest\n'
               '{mountain} mountain').format(total=total,
                                             woods=woods,
                                             forest=forest,
                                             mountain=mountain)
        super().__init__(msg, *args, **kwargs)
