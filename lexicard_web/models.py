import os

from django.db import models
from django_resized import ResizedImageField


def profile_picture_dir(i, f):
    return os.path.join(f"assets/{i.user_id}", f)

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=256, blank=True)

    USERNAME_FIELD = 'username'


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user_image =ResizedImageField(size=[256, 256], upload_to=profile_picture_dir, blank=True, force_format='JPEG')

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    document_name = models.CharField(max_length=128, blank=True)

    FILE_FORMAT = [
        ("PPT", "Microsoft Powerpoint File"),
        ("PPTX", "Microsoft Powerpoint File"),
        ("DOC", "Microsoft Word File"),
        ("DOCX", "Microsoft Word File"),
        ("RTF", "Rich Text Format"),
    ]

    document_format = models.CharField(max_length=16, choices=FILE_FORMAT, default=None)

class Deck(models.Model):
    deck_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, null=False)
    deck_name = models.CharField(max_length=128, blank=True)

class Flashcard(models.Model):
    flashcard_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    deck_id = models.ForeignKey(Deck, on_delete=models.CASCADE, null=False)

class QA(models.Model):
    flashcard_id = models.ForeignKey(Flashcard, on_delete=models.CASCADE, null=False)
    flashcard_question = models.CharField(max_length=512, blank=True)
    flashcard_answer = models.CharField(max_length=512, blank=True)

class Reminders(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reminder_name = models.CharField(max_length=64, blank=True)
    reminder_label = models.CharField(max_length=64, blank=True)
    reminder_start_timestamp = models.DateTimeField(auto_now_add=True)
    remidner_end_timestamp = models.DateTimeField(blank=True)


