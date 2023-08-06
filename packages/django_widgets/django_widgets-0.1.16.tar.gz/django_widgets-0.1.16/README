
# Autocomplete and button group select widgets in django

An alternative to RadioSelect, where all values are populated but hidden as a `ul > li` list in html. The user can
type in a textbox, and when the text matches one of the labels of the choices, the list item are displayed.

This avoids ajax.


## Setup

    pip install django_widgets

Include these static files in your `<head>`

    <link rel="stylesheet" href="{% static 'django-widgets.css' %}"/>
    <script src="{% static 'django-widgets.js' %}"></script>

Django 'INSTALLED_APPS'

    INSTALLED_APPS = (
        # ...
        'django_widgets',
        # ...
    )

A form:

    class TestForm(forms.Form):
        value = forms.ChoiceField(
            choices=[(5, 'Vijf'), (6, 'Zes'), (7, 'Zeven'), (18, 'Achttien'), (14, 'Veertien')],
            widget=AutocompleteSelect
        )

## Result

![Example widget][example]

[example]: example.png "Example widget"
