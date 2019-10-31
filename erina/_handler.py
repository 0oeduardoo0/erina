import unidecode
from ._input import Command, Args


class Handler():
    """Base class to handlers.

    Handlers will receive the incoming messages and they will do
    something if they recognize some command.

    Attributes:
        attachments (array): fbchat attachments array
        type (str): "text" or attachment type ("image", "audio"...)
        response (Response): Response instance (ready to send messages yey)
        command (Command): command instance of input (just command)
        args (Args): args instance of input (just arguments)
        raw_input (Command): command instance containig full message input
    """

    def __init__(self, msg, response):
        """Parses the input message.

        Handler instaces are instanced by Bot class when
        some message are received. Cronjob also instaces
        Handler classes but it doesn't gives msg and
        response params.

        Args:
            msg (Message): fbchat message  object
            response (Response): Response object
        """
        if not msg and not response:
            return

        self.attachments = msg.attachments

        if msg.text:
            self.type = "text"

            # remove special chars like spanish accents
            if type(msg.text) is unicode:
                msg.text = unidecode.unidecode(msg.text)

            self.raw_input = Command(msg.text)

            splitted = msg.text.split(" ")

            self.command = Command(splitted[0])

            if len(splitted) > 1:
                splitted.pop(0)
                self.args = Args(splitted)

            else:
                self.args = Args([])

        else:
            self.type = self.attachments[0].type

        self.response = response

    def cron(self, time):
        """Called by cronjob.

        If you register a handler as cronjob, cron will call this method
        every minute.

        Args:
            time (datetime): datetime object
        """
        pass

    def handle(self):
        """ Called by Bot class.

        It must return True if the incoming command is recognized and executed.
        """
        pass


class DefaultHandler(Handler):
    """Default handler.

    It will response if all the other registered handlers didn't.
    """

    def handle(self):
        """Default response to every single text message.
        """
        if self.type == "text":
            self.response.text('mmm...?')
            return True
