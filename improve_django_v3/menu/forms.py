from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu


class MenuForm(forms.ModelForm):

    # expiration_date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]

    def clean_items(self):
        items = self.cleaned_data['items']
        return items
