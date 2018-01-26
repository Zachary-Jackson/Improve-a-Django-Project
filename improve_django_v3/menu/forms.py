import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu


def two_years_from_now():
    '''This returns a date object that is two years from the time
    this function is ran.'''
    today = datetime.datetime.now().date()
    today += datetime.timedelta(730)
    return today


class MenuForm(forms.ModelForm):

    expiration_date = forms.DateField(
        widget=SelectDateWidget, initial=two_years_from_now()
    )

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
        ]
