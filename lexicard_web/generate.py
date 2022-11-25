from PIL import Image, ImageFont, ImageDraw
import io
import textwrap
import zipfile
import tarfile

class Generate():

    def __init__(self, width: int = 720, height: int = 480):
        self.width = width
        self.height = height

        # Set font family and size
        self.font1 = ImageFont.truetype("./static/times.ttf", 32)
        self.font2 = ImageFont.truetype("./static/times.ttf", 24)
        self.font3 = ImageFont.truetype("./static/times.ttf", 16)

        # Font 4 is for the question card
        self.font4 = ImageFont.truetype("./static/times.ttf", 40)

        # Initialize background images
        self.background = Image.open("./static/flashcard-template.png")
        self.question = Image.open("./static/flashcard-template.png")

        # Draw/create blank white image
        self.I1 = ImageDraw.Draw(self.background)
        self.I2 = ImageDraw.Draw(self.question)


    # Set term
    def set_term(self, term: str):
        self.I1.text(
            (self.width * 0.0694, self.height * 0.108),
            term,
            font=self.font1,
            fill=(0, 0, 0),
            resample=Image.ANTIALIAS
        )

    # Add definition and text wrapping
    def set_definition(self, definition: str, width: int = 60):
        offset_w = self.width * 0.0694
        offset_h = self.height * 0.3

        for line in textwrap.wrap(definition, width=width):
            self.I1.text(
                (offset_w, offset_h),
                line,
                font=self.font2,
                fill=(0, 0, 0),
                resample=Image.ANTIALIAS
            )

            offset_h += self.font2.getsize(line)[1]

    def save_image(self, response):
        return self.background.save(response, "PNG")

    def save_zip(self, user_id, deck_id, response, question_list, answer_list):
        # Overwrite file to an empty zip file
        with zipfile.ZipFile(f"flashcard_{user_id}_{deck_id}.zip", "w") as zf:
            pass

        counter = 1
        zip_in_memory = io.BytesIO()
        with zipfile.ZipFile(zip_in_memory, "a") as zf:
            for i, j in zip(question_list, answer_list):
                flashcard = Generate()
                flashcard.set_term(i)
                flashcard.set_definition(answer_list)
                zf.writestr(f"{counter}.png", self.background.tobytes())

        # Return zip type data
        return zf


