"""Erina (facebook messenger chatbot)

:copyright: (c) 2019 Eduardo Becerril
:license: GNU/GPL v3, see LICENSE for more details.
"""

from ._bot import Bot
from ._log import log, chatlog, setLogFile
from ._handler import Handler, DefaultHandler
from ._environment import Environment
from ._notify_service import NotifyService
from ._response import Response
from ._notification import Notification, TextNotification, ImageNotification, RemoteImageNotification
from ._speech_recognition import SpeechRecognition
from ._input import Command, Args
from ._attachments import Attachments
from ._miscellaneous import startMessage

__title__ = "erina"
__version__ = "1.0.0"
__description__ = "facebook messenger chabot"

__copyright__ = "Copyright 2019 Eduardo Becerril"
__license__ = "GNU/GPL v3"

__author__ = "Eduardo Becerril"
__email__ = "ms7rbeta@gmail.com"
