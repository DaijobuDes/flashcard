"""
This file implements password validation for
django's AUTH_PASSWORD_VALIDATORS. Custom made
classes in order to validate and return an exception
if a condition does not meet the requirement.

Each validate() method raises a ValidationError if
data does not match with its regex.

See https://docs.djangoproject.com/en/4.0/topics/auth/passwords/
for more details.
"""

import re

from django.core.exceptions import ValidationError

class NumberValidator(object):
   """Check if a number exists"""
   def validate(self, password, user=None):
      if not re.findall('\d', password):
         raise ValidationError("The password must contain at least 1 digit, 0-9.")

