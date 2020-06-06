from PIL import Image, ImageDraw, ImageFont


class TransformationImage:
    def __init__(self, image):
        self.image = Image.open(image)
        self.image.thumbnail((720, 1280), Image.ANTIALIAS)
        self.image.load()
        self.height_image = self.image.height
        self.width_image = self.image.width

        self.height_block = 100

    def add_panel_text(self, text):
        draw = ImageDraw.Draw(self.image, "RGBA")
        draw.polygon([(0, self.height_image / 2), (0, self.height_image / 2 + self.height_block),
                      (self.width_image, self.height_image / 2 + self.height_block),
                      (self.width_image, self.height_image / 2)],  fill=(255, 170, 228, 120))
        font = ImageFont.truetype("KateBot/static/fonts/Montserrat_Black.ttf", 50)
        #  text = "16 дней 10:23:23"
        size = font.getsize(text)
        draw.text((self.width_image / 2 - size[0] / 2, (self.height_image / 2 - 13) + size[1] / 2),
                  text=text, fill="white", font=font)
        self.image.save("KateBot/static/ready_image.jpeg")
