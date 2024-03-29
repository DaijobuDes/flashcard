import os
from hashlib import md5

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone

# Reference
# http://www.learningaboutelectronics.com/Articles/How-to-rename-an-image-or-file-in-an-upload-Django.php
# https://web.archive.org/web/20230103172715/http://www.learningaboutelectronics.com/Articles/How-to-rename-an-image-or-file-in-an-upload-Django.php
def profile_picture_dir(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    hashed_filename = md5(base_filename.encode()).hexdigest()
    return f"profile/{hashed_filename}{file_extension}"

def document_dir(instance, filename):
    base_filename, file_extension = os.path.split(filename)
    hashed_filename = md5(base_filename.encode()).hexdigest()
    return f"documents/{hashed_filename}{file_extension}"

# Create your models here.
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=32, blank=True, unique=True)
    email = models.CharField(max_length=128, blank=True, unique=True)
    password = models.CharField(max_length=256, blank=True)
    notifs = models.BooleanField(default=False)

    term_bg_color = models.CharField(max_length=7, blank=True, default="#FF0000")
    term_txt_color = models.CharField(max_length=7, blank=True, default="#FFFFFF")
    question_bg_color = models.CharField(max_length=7, blank=True, default="#0000FF")
    question_txt_color = models.CharField(max_length=7, blank=True, default="#FFFFFF")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = BaseUserManager()

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    message_body = models.CharField(max_length=256, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user_image = ResizedImageField(size=[512, 512], upload_to=profile_picture_dir, blank=True, force_format='JPEG')

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
        ("TXT", "Text File Format"),
        ("PDF", "Portable Document Format"),
    ]
    document_file = models.FileField(upload_to=document_dir, max_length=100)
    document_format = models.CharField(max_length=16, choices=FILE_FORMAT, default=None)
    date_modified = models.DateTimeField(default=timezone.now)

    @property
    def filesize(self):
        x = self.document_file.size

        if x < 512000:
            value = round(x/1024, 2)
            ext = ' Kb'
        elif x < 4194304000:
            value = round(x/1048576.0, 2)
            ext = ' Mb'
        else:
            value = round(x/1073741824, 2)
            ext = ' Gb'
        return str(value)+ext


class Classes(models.Model):
    classes_id = models.AutoField(primary_key=True)
    classes_name = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    def __int__ (self):
      return self.classes_id

class Deck(models.Model):
    deck_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, null=False)
    deck_name = models.CharField(max_length=128, blank=True)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, null=False)

class Flashcard(models.Model):
    flashcard_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    deck_id = models.ForeignKey(Deck, on_delete=models.CASCADE, null=False)

class QA(models.Model):
    QA_id = models.AutoField(primary_key=True)
    flashcard_id = models.ForeignKey(Flashcard, on_delete=models.CASCADE, null=False)
    flashcard_question = models.CharField(max_length=512, blank=True)
    flashcard_answer = models.CharField(max_length=512, blank=True)

class Reminders(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reminder_name = models.CharField(max_length=64, blank=True)
    reminder_label = models.CharField(max_length=64, blank=True)
    reminder_created_timestamp = models.DateTimeField(auto_now_add=True)
    reminder_timestamp = models.DateTimeField(blank=True)



