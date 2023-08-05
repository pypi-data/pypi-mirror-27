#!/usr/bin/env python

import re

from django.core.validators import RegexValidator
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy as _

from widgets import TinyColorPickerWidget


# Validation for hex colors
COLOR_REGEX = re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
COLOR_VALIDATOR = RegexValidator(COLOR_REGEX, _('Enter a valid color.'), 'invalid')



class TinyColorPickerField(Field):
	widget = TinyColorPickerWidget
	default_validators = [COLOR_VALIDATOR,]
