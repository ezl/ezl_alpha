from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField

from units.models import Unit

class UnitCreationForm(forms.ModelForm):
    zipcode = USZipCodeField(required=False)

    class Meta:
        model = Unit
