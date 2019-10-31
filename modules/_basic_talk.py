import urllib2
from bs4 import BeautifulSoup

from erina import Handler


class BasicTalk(Handler):

    def chiste(self):
        try:
            url = "http://www.chistes.com/chistealazar.asp"
            page = urllib2.urlopen(url, timeout=5)
            soup = BeautifulSoup(page, 'html.parser')
            box = soup.find('div', attrs={'class': 'chiste'})
            chiste = box.text

        except urllib2.URLError, e:
            chiste = False

        return chiste

    def handle(self):
        if self.type == "text":
            if self.raw_input.eq("<unrecognized audio>"):
                self.response.text("Lo siento, no entendi lo que dijiste :(")
                return True

            if self.raw_input.has(3, "que", "sabes", "puedes", "hacer"):
                self.response.text("Muchas cosas wuu xd")
                self.response.text("Puedes hablarme por audios :3")
                self.response.text("Me se algunos chistes jeje")

            if self.raw_input.has(1, "hola", "holi", "hello"):
                self.response.text("Hola :)")

            if self.raw_input.has(2, "buen", "dia", "tarde", "noche"):
                self.response.text("Buenas :)")

            if self.raw_input.has(2, "como", "estas"):
                self.response.text("Solo soy un robot, pero bien, gracias :3")

            if self.raw_input.has(1, "ty", "thanks", "gracias"):
                self.response.text("No hay de que ^u^")

            if self.raw_input.has(2, "quien", "eres", "como", "llamas", "cual", "nombre"):
                self.response.text("Hola, mi nombre es Erina, soy un robot jeje :3")

            if self.raw_input.has(1, "jaja", "jeje", "haha", "hehe"):
                self.response.text("que es tan gracioso? :)")

            if self.raw_input.has(2, "tu", "eres", "graciosa", "linda", "divertida", "inteligente"):
                self.response.text("jaja gracias")

            if (
                self.raw_input.has(2, "chiste", "cuenta", "divertido", "escuchar", "oir", "reir", "algo", "di", "risa", "cuentes", "contar", "un")
                or self.command.eq("chiste")
                ):
                chiste = self.chiste()

                self.response.text("mmm... a ver...")

                if chiste:
                    self.response.text(chiste)
                    self.response.text("JAJAJAJAJAJAJAJA :')")

                else:
                    self.response.text("no se me ocurre nada por ahora xd")

                return True

        return False
