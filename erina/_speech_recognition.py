import os
import urllib
from pydub import AudioSegment
import speech_recognition as sr


class SpeechRecognition():
    """Speech recognition utility."""
    def __init__(self):
        """Initializes recognizer.
        """
        self.recognizer = sr.Recognizer()

    def downloadAudio(self, name, audio_message):
        """ Downloads remote audio.

        This method will download audio files from audio attachments.
        """
        mp4 = "%s.mp4" %(name) # facebook uses mp4 audio files .-.
        wav = "%s.wav" %(name) # but audio recognizer needs wav

        urllib.urlretrieve(audio_message.url, mp4)

        # so after download the audio we gonna convert it to wav
        sound = AudioSegment.from_file(mp4, "mp4")
        sound.export(wav, format="wav")

        os.remove(mp4) # we don't need mp4
        return wav

    def recognize(self, author, audio_message):
        """Converts an audio message to text (speech to text).

        Args:
            author (str): author id (who sent the message)
            audio_message (AudioAttachment): fbchat audio message

        Returns:
            str: recognized (maybe) text
        """
        file = "_data/SpeechRecognition/%s" %(author)
        audio = self.downloadAudio(file, audio_message)

        with sr.AudioFile(audio) as source:
            audio = self.recognizer.record(source)

        return self.recognizer.recognize_google(audio, language="es-MX")
