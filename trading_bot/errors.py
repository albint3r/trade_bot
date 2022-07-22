class MissingConfigError(Exception):

    def __init__(self, config: object):
        self.c = config

    def __str__(self):
        return f'You most create a Config (from_object) File or fill: API_SECRETE -> {self.c.get("API_KEY")}, SECRET_KEY -> {self.c.get("API_KEY")}'


class NoExistClientError(Exception):

    def __str__(self):
        return f'You most create a CREATE A CLIENT'
