from ._image_filter import ImageFilter
from ._basic_talk import BasicTalk
from ._random_meme import RandomMeme
from ._notify_service_test import NotifyServiceTest

handlers = [
    ImageFilter,
    RandomMeme,
    BasicTalk
]

cronjobs = [
    NotifyServiceTest
]
