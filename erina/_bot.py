import os
import json
import logging

from fbchat.models import *
from fbchat import Client, Message, FBchatUserError

from ._log import log, chatlog
from ._handler import DefaultHandler
from ._response import Response
from ._attachments import Attachments
from ._speech_recognition import SpeechRecognition
from ._notify_service import NotifyService
from ._environment import Environment
from ._miscellaneous import startMessage


class Bot(Client):
    """Bot class.

    This is the main class of 'erina', it inherit 'fbchat' client class,
    this class inits fbchat and erina's notify service socket. Also it will
    handle incoming messages from fbchat and parse the input messages and
    it will send them to handlers.
    """

    def __init__(self, credentials=None):
        """Initialize some vars and fbchat login.

        Args:
            credentials (dict): 'user' and 'passw' to log into facebook
        """
        if not credentials:
            log.warning("no credentials set")
            return

        self.env = Environment()
        self.attachments = Attachments()
        self.speech_recognition = SpeechRecognition()
        self.notify_service = NotifyService()

        self.request_handlers = []
        self.default_request_handler = DefaultHandler

        user = credentials['user']
        passw = credentials['passw']
        # we get the session cookies from environment vars
        session_cookies = self.env.get("session_cookies")

        # notify_subscriptions is an array of fb user ids, users on this list
        # will receive notifications from the notify service
        self.notify_subscriptions = self.env.get("notify_subscriptions")

        try:

            super(Bot, self).__init__(user, passw, session_cookies=session_cookies)
            # if logging with cookies failed we need to set the new cookies
            self.env.set("session_cookies", super(Bot, self).getSession())

        except FBchatUserError:

            log.warning("Login failed")

    def setDefaultHandler(self, handler):
        """Set default request handler.

        Default handler is the handler which handle the input request
        if all the others handlers didn't.

        Args:
            handler (Handler): default handler
        """
        self.default_request_handler = handler

    def addHandler(self, handler):
        """Adds a handler

        Args:
            handler (Handler): handler to add
        """
        self.request_handlers.insert(0, handler)

    def onNotify(self, notification):
        """Function to handle incoming notifies.

        Notifies are messages to send to users in notify subscription list.
        This messages comes from notify service listener.

        Args:
            type (str): "text" for text messages and "image" for image messages
            content (str): message content.
        """
        users = self.fetchAllUsers()

        for user in users:
            # only notify if user (id) is in subscription list
            if user.uid in self.notify_subscriptions:
                res = Response(self, user.uid, user.type)

                log.info("notification received %s" %(notification.toJsonString()))
                notification.execute(res)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        """Handles incoming messages (from facebook).

        This function its called from fbchat when somebody sends a message.

        Args:
            author_id: The ID of the author
            message_object (Message): The message (As a `Message` object)
            thread_id: Thread ID that the message was sent to.
            thread_type (ThreadType): Type of thread that the message was sent to.
        """
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        if author_id != self.uid:
            try:
                user = self.fetchUserInfo(author_id)
                user_name = user[author_id].first_name

            except:
                user_name = author_id


            if message_object.attachments:

                reset_attachments_storange_flag = False

                for item in message_object.attachments:
                    chatlog.info("[<-][%s] %s" % (user_name, item.__class__.__name__))

                    # if the attachment is an image we just put it in
                    # attachments (attachments are associated with an specific user)
                    if self.attachments.type(item) != "audio":
                        # we can get a batch of images in the same message
                        # so we just reset the attachments storage for the
                        # first image of the batch
                        if not reset_attachments_storange_flag:
                            self.attachments.reset(author_id)
                            reset_attachments_storange_flag = True

                        item.url = self.fetchImageUrl(item.uid)
                        self.attachments.add(author_id, item)

                    # if we have and audio message we try speech to text
                    # notice that we dont reset attachment storage cuz
                    # come command could need files in the storage to do
                    # something
                    else:
                        try:
                            text = self.speech_recognition.recognize(author_id, item)
                        except:
                            text = "<unrecognized_audio>"

                        # if the recognition success, we set it as incoming message text
                        message_object.text = text

            # this flag will be used to know
            # when a handler served the request succesfully
            # if it is set to True the loop which executes
            # handlers will be stoped
            served = False
            res = Response(self, thread_id, thread_type)

            message_object.attachments = self.attachments.get(author_id)

            for req_class in self.request_handlers:
                req = req_class(message_object, res)
                served = req.handle()

                if served:
                    break

            if not served:
                req = self.default_request_handler(message_object, res)
                req.handle()

            chatlog.info("[<-][%s] %s" % (user_name, message_object.text))

        else:
            chatlog.info("[->][Erina] %s" % (message_object.text))

    def listen(self):
        """Starts fbchat and notify service listeners.
        """
        log.info(startMessage())

        self.notify_service.setNotifyHandler(self.onNotify)
        self.notify_service.listen()
        super(Bot, self).listen()
