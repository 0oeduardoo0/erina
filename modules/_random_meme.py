import urllib2
import random
from bs4 import BeautifulSoup

from erina import Handler


class RandomMeme(Handler):

    def momazo(self):
        try:
            n = random.randint(1, 200)
            url = "https://es.memedroid.com/memes/random/%s" %(n)
            hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
            }

            req = urllib2.Request(url, headers=hdr)

            page = urllib2.urlopen(req, timeout=5)
            soup = BeautifulSoup(page, 'html.parser')
            boxes = soup.findAll('article', attrs={'class': 'gallery-item'})

            n = random.randint(0, len(boxes))
            img = boxes[n].find('img')

            meme = img['src']
            return meme

        except urllib2.URLError, e:
            return False

    def handle(self):
        if self.type == "text":
            if self.raw_input.has(3, "que", "sabes", "puedes", "hacer"):
                self.response.text("Tengo buenos momazos :D")

            if (
                self.raw_input.has(2, "meme", "momo", "momi", "moma", "manda", "muestra", "ense", "a ver", "envia") or
                self.command.eq("meme", "momo", "momazo", "momingo")
                ):
                self.response.text("Deja veo si tengo uno ^u^")
                momo = self.momazo()

                if momo:
                    self.response.remote_image('', momo)
                    self.response.text("Que tal xD?")

                else:
                    self.response.text("No tengo momazos por ahora :(")

                return True
