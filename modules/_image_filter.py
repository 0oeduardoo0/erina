import numpy as np
import urllib
import cv2

from erina import Handler


class ImageFilter(Handler):

    def readFromUrl(self, url):
        resp = urllib.urlopen(url)

        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image

    def handle(self):
        if self.type == "text":
            if self.raw_input.has(3, "que", "sabes", "puedes", "hacer"):
                self.response.text("Puedes mandarme una foto y puedo hacer algunas cosas con ella B)")

            if (
                self.raw_input.has(2, "filtro", "efecto", "blanco", "negro", "bn", "desenfoque", "blur", "negativo") or
                self.raw_input.has(1, "desenfoca", "desenfocar", "desenfoques")
                ):
                if self.attachments:
                    self.response.text("okis dame un segundo")

                    applied = False

                    for item in self.attachments:
                        if item.type == "image":
                            image = self.readFromUrl(item.url)

                            if self.raw_input.has(1, "blanco", "negro", "bn"):
                                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                            elif self.raw_input.has(1, "blur", "desenfoque", "desenfoca", "desenfocar", "desenfoques"):
                                image = cv2.blur(image, (10, 10))

                            elif self.raw_input.has(1, "negativo"):
                                image = (255-image)

                            image_file = './_data/ImageFilter/%s.jpg' %(item.author)

                            cv2.imwrite(image_file, image)

                            self.response.image("", image_file)
                            applied = True

                        else:
                            self.response.text("Necesito imagenes :)")

                    if applied:
                        self.response.text("Listo :D")

                else:
                    self.response.text("Envia primero algunas imagenes")

                return True

            elif self.raw_input.has(2, "filtros", "tienes", "lista", "imagen", "aplicas", "que", "como", "cuales"):
                self.response.text("Tengo filtro blanco y negro, negativo y desenfoque :)")
                return True

        elif self.type == "image":
            self.response.text("Puedo aplicar algunos filtros a tus imagenes ^u^")

        return False
