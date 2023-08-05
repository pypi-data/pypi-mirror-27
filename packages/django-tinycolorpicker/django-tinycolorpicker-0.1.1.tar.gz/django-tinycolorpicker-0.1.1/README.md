# django-tinycolorpicker
Django Field and Widget implementation of [wieringen/tinycolorpicker](https://github.com/wieringen/tinycolorpicker)

## Installation
django-tinycolorpicker is available on pypi here: https://pypi.python.org/pypi/django-tinycolorpicker

It also must be added to `INSTALLED_APPS` so that its static files will be collected.

## Usage

### Simplest best practice example

```python
from tinycolorpicker.fields import TinyColorPickerField

class MyForm(forms.Form):
    color = TinyColorPickerField()
```

In general, no change to your templates is necessary (if you're using `{{ form.media }}` or similar). Otherwise, you'll need to include the tinycolorpicker library manually in your base template or similar:

```html
<link href="/static/tinycolorpicker/css/tinycolorpicker.css" type="text/css" media="all" rel="stylesheet" />
<script type="text/javascript" src="/static/tinycolorpicker/js/tinycolorpicker.js"></script>
```



## Settings and Their Overrides

| Setting                 | Kwarg           | Description                        | Valid Values | Default Value |
| ------------------------|-----------------|------------------------------------|--------------|---------------|
| TINYCOLORPICKER_IMAGE   | image           | relative path vis-a-vis STATIC_URL |              | tinycolorpicker/img/text-color.png |
| TINYCOLORPICKER_VARIANT | variant         | whether to use the vanilla js or jquery version | 'vanilla' or 'jquery' | 'vanilla' |


Settings can be overridden as kwargs when instantiating TinyColorPickerWidget

Additionally, if DEBUG is True, the form media as rendered by {{ form.media }} or similar, will be the unminified versions.
