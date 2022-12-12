from django import forms
from .models import *

class UserForm(forms.Form):
   """
   A class used for user registration
   """

   username = forms.CharField()
   email = forms.EmailField(widget=forms.EmailInput())
   password = forms.CharField(widget=forms.PasswordInput())

   class Meta:
      """
      Class metadata for UserForm
      """
      model = User
      fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
   """
   A class used for user login
   """

   username = forms.CharField()
   password = forms.CharField(widget=forms.PasswordInput())

   class Meta:
      """
      Class metadata for UserForm
      """
      model = User
      fields = ['username', 'password']


class UpdateProfile(forms.Form):
   """
   A class used for updating the user's profile page.
   """

   pass

""" Document Forms """
class DocumentForm(forms.ModelForm):
   """
   A class used for manipulating documents.
   """
   class Meta:
      """ 
      Class metadata for UserForm 
      """
      model = Document
      fields = ['user_id', 'document_name', 'document_file', 'document_format']

class UploadDocForm(forms.Form):
   """
   A class used for uploading documents.
   """
   doc_file = forms.FileField()
   doc_format = forms.CharField()

   class Meta:
      """ 
      Class metadata for UserForm 
      """
      model = Document
      fields = ['user_id', 'document_name', 'document_file', 'document_format']


""" Schedule Forms """
class ScheduleForm(forms.Form):
   """
   A class used for manipulating reminders.
   """
   class Meta:
      """ 
      Class metadata for ScheduleForm 
      """
      model = Reminders
      fields = ['user_id', 'reminder_name', 'reminder_label', 'reminder_created_timestamp', 'reminder_timestamp']

