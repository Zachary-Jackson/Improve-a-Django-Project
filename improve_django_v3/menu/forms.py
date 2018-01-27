import datetime
import string

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

    hidden_field = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
        ]

    def clean_hidden_field(self):
        '''This creates a honeypot to get rid of some bots.'''
        hidden_field = self.cleaned_data['hidden_field']
        if hidden_field == '':
            return hidden_field
        else:
            raise forms.ValidationError("Take that bot!")

    def clean_season(self):
        '''This makes sure that season does not contain punctuation
        except for apostrophe.'''
        season = self.cleaned_data['season']
        punctuation_less_apostrophe = [letter for letter in string.punctuation]
        punctuation_less_apostrophe.remove("'")
        ''.join(punctuation_less_apostrophe)
        for character in season:
            if character in punctuation_less_apostrophe:
                raise forms.ValidationError(
                    "You can not have any punctuation except for" +
                    " apostrophes.")
        return season
