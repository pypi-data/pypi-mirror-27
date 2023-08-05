#!/usr/bin/env python

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.forms.widgets import Input



class TinyColorPickerWidget(Input):
	input_type = 'text'
	template_name = 'tinycolorpicker/widget.html'

	def __init__(self, attrs=None, image=None, variant=None):
		super(TinyColorPickerWidget, self).__init__(attrs=attrs)
		self.image = image or getattr(settings, 'TINYCOLORPICKER_IMAGE', 'tinycolorpicker/img/text-color.png')
		self.variant = variant or getattr(settings, 'TINYCOLORPICKER_VARIANT', 'vanilla')


	def get_context(self, name, value, attrs):
		context = super(TinyColorPickerWidget, self).get_context(name, value, attrs)
		context['widget']['image'] = self.image
		context['widget']['variant'] = self.variant
		return context


	@property
	def media(self):
		if self.variant == 'vanilla':
			if settings.DEBUG:
				js = ['tinycolorpicker/js/tinycolorpicker.js',]
			else:
				js = ['tinycolorpicker/js/tinycolorpicker.min.js',]
		elif self.variant == 'jquery':
			if settings.DEBUG:
				js = ['tinycolorpicker/js/jquery.tinycolorpicker.js',]
			else:
				js = ['tinycolorpicker/js/jquery.tinycolorpicker.min.js',]
		else:
			raise ImproperlyConfigured("TINYCOLORPICKER_VARIANT must be one of 'vanilla' or 'jquery'")

		css = ['tinycolorpicker/css/tinycolorpicker.css',]
		return forms.Media(css={'all': css}, js=js)
