class ComilioException(Exception):
    payload = None

class InvalidCredentials(ComilioException): pass

class InsufficientCredit(ComilioException): pass
