from django import forms
from .models import *

class UserForm(forms.Form):
   """
   A class used for login
   """

   email = forms.EmailField(widget=forms.EmailInput())
   password = forms.CharField(widget=forms.PasswordInput())

   class Meta:
      """
      Class metadata for UserForm
      """
      model = User
      fields = ['email', 'password']


class RegistrationForm(forms.Form):
    """
    A class used for user registration
    """

    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        """
        Class metadata for RegistrationForm
        """
        model = User
        fields = ['username', 'email', 'password']