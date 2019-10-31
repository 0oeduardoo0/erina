import threading
import socket

from ._log import log
from ._environment import Environment
from ._notification import Notification


class NotifyService():
    """Notification service class

    This class doesn't check notify_subscriptions, Bot class does. This class
    just establish a comunication channel between erina's bot (listener) and
    external programs (such as cronjobs) to send messages.
    """

    def __init__(self):
        """Initialize some vars.
        """
        self.env = Environment()
        self.notify_handler = None

        self.host = self.env.get("notify_service_host")
        self.port = self.env.get("notify_service_port")

    def send(self, notification):
        """Send data to notify service listener.

        Args:
            notification (str): data to send
        """
        data = notification.toJsonString()
        log.info("sending notification %s" %(data))
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))
            client.send(data)
            client.close()
        except:
            log.warning("error when connecting to notify service listener")
            pass

    def serverTrhead(self):
        """Starts listener loop.

        Listener is a TCP socket inside a loop. So we need to run it in an
        independent thread.
        """
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server.bind((self.host, self.port))
            server.listen(1)
        except:
            log.warning("Error starting notify service!")
            log.warning("Is address already in use?")
            return

        log.info("Notification service listening...")

        try:
            while True:
                client, port = server.accept()

                data = ""
                while True:
                    _data = client.recv(1024)

                    if _data:
                        data += _data

                    else:
                        break

                if self.notify_handler:
                    notification = Notification()
                    notification.fromJsonString(data)
                    self.notify_handler(notification)

                else:
                    log.info("notify_handler is not set")
                    log.info("%s" %(full_data))

        except KeyboardInterrupt:
            log.info("interrupt received, stopping notify service")

        finally:
            server.shutdown(socket.SHUT_RDWR)
            server.close()

    def setNotifyHandler(self, notify_handler):
        """Sets notify handler.

        Args:
            notify_handler (callable): notify handler, it must be receive 2 args
                                       type (str) and data (str)
        """
        self.notify_handler = notify_handler

    def listen(self):
        """Starts notify service listener.
        """
        th = threading.Thread(target=self.serverTrhead)
        th.start()
