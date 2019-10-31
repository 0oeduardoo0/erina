import time
from fbchat import Message, TypingStatus

class Response():
    """Response facility (easy way to send fbchat messages)

    This class a comunication channel to send messages to some user.
    This class is normally initialized by Bot class.
    """
    def __init__(self, fbchat, thread_id, thread_type):
        """Sets instence attributes.

        Args:
            fbchat (Client): fbchat client instance
            thread_id (str): user or group id
            thread_type (int): thread type
        """
        self.fbchat = fbchat
        self.tid = thread_id
        self.ttype = thread_type

    def text(self, msg):
        """Sends a text message.

        Args:
            msg (str): message to send
        """
        self.typing()
        self.fbchat.send(Message(text=msg),thread_id=self.tid, thread_type=self.ttype)

    def image(self, msg, img):
        """Sends an image message.

        Args:
            msg (str): message text that will be sent with the image
            img (str): image path
        """
        self.typing()
        self.fbchat.sendLocalImage(
            img,
            message=Message(text=msg),
            thread_id=self.tid,
            thread_type=self.ttype
        )

    def remote_image(self, msg, url):
        """Sends a image (from remote source) message.

        Args:
            msg (str): message text that will be sent with the image
            url (str): remote image url
        """
        self.typing()
        self.fbchat.sendRemoteImage(
            url,
            message=Message(text=msg),
            thread_id=self.tid,
            thread_type=self.ttype
        )

    def typing(self):
        """Sets writing status as typing and wait half second.
        """
        self.fbchat.setTypingStatus(
            TypingStatus.TYPING,
            thread_id=self.tid,
            thread_type=self.ttype
        )

        time.sleep(0.5)
