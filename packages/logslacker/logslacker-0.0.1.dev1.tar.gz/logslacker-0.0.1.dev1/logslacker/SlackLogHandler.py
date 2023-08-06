from logging import Handler

from slackclient import SlackClient

class SlackLogHandler(Handler):
    def __init__(self):
        self.text = "Just testing ATM."

    def test(self):
        return self.text
