class GxbRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'GxbRequestException: %s' % self.message
