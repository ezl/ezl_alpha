from django import forms

from rentals.models import Rental

class RentalCreationForm(forms.ModelForm):
    # start_date = forms.DateField(required=False, widget=forms.DateInput)
    # end_date= forms.DateField(required=False)

    class Meta:
        model = Rental
        exclude = ('creator',)

