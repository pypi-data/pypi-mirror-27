from slacker import Slacker
import os

class BrewerBot(Slacker):
    """
    A wrapper around the slacker package.

    Write slack webhook into `~/slack.token`, and set environment variable `brewer_channel`
    to the desired channel. You may also set the slack webhook as an environment variable called `brewer_token`.
    Env variable takes precedence over file.
    """
    def __init__(self):
        self.token_file = os.path.expanduser("~") + "/slack.token"
        self.token = self.get_token()
        self.slacker = Slacker(self.token)
        self.channel = os.getenv('brewer_channel', '@luke')

    def get_token_from_file(self):
        """
        Read the slack webhook from `~/slack.token`
        """
        with open(self.token_file, "r") as file:
            # FIXME: Boot up brewer_network if there's no token??
            return file.readlines()[0].rstrip()

    def get_token(self):
        """
        Try to get the token from the environment variable.
        """
        return os.getenv('brewer_token', self.get_token_from_file())

    def send(self, message):
        """
        Send a message in the configured slack channel.
        """
        # I don't want to mess around with 'super'. It's confusing and I don't have time.
        self.slacker.chat.post_message(self.channel, message, username = "Beer Bot")
        return True
