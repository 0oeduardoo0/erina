import json


class Notification():
    """Class that represents a notification.

    These notificatios travel between Notification service (throw sockets)
    and externals programs (such as cronjobs) which sends notificatios.
    """

    def fromJsonString(self, json_str):
        """Sets notification data from json_str.

        Args:
            json_str (str): Notification data (json string) to decode
        """
        self.notification = json.loads(json_str)

    def toJsonString(self):
        """Gets notification data encoded as json string.

        Returns:
            str: notification data as json string
        """
        return json.dumps(self.notification)

    def execute(self, respose):
        """Sends the notification.

        The notification (message) will send to users throw Response.

        Args:
            respose (Response): respose to send notification
        """
        if self.notification['type'] == "text":
            respose.text(self.notification['data'])

        elif self.notification['type'] == "image":
            respose.image("", self.notification['data'])

        elif self.notification['type'] == "remote-image":
            respose.remote_image("", self.notification['data'])


class TextNotification(Notification):
    """Represents a text notification
    """

    def __init__(self, data):
        """Sets notification data for text messages.

        Args:
            data (str): text of the message
        """
        self.notification = {
            "type": "text",
            "data": data
        }


class ImageNotification(Notification):
    """Represents a local image notification.
    """

    def __init__(self, path):
        """Sets notification data for local image messages.

        Args:
            path (str): path to image
        """
        self.notification = {
            "type": "image",
            "data": path
        }


class RemoteImageNotification(Notification):
    """Represents a remote image notification.
    """

    def __init__(self, url):
        """Sets notification data for remote image messages.

        Args:
            url (str): image url
        """
        self.notification = {
            "type": "remote-image",
            "data": url
        }
