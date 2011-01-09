from django import forms

from rentals.models import Rental
from accounts.models import Broker

class RentalSelectionForm(forms.Form):
    """1. Form for applicant to select the Rental property he/she is interested in"""
    """2. Repurposing this to also use to select rentals to add to the list of units
       represented by an Agency"""
    """These uses should BOTH disappear (along with the Form class) once out of demo.
       1. There should be no case for the applicant to choose from a list of rentals.
          -- if they have a hash and get it wrong, they need to get it again from the
             broker to make sure its right.  we'll display an error message saying
             "try again".  if we let the user "select" from a list, we won't know
             what rentals to show.
          -- if they don't have a hash, we'll ask them to create the rental or request
             for the rental, or to tell the landlord/broker to do it.
       2. Agencies don't have access to all the rentals in the world.  its not a pulldown,
          there is only creation and deletion."""
    rental = forms.ModelChoiceField(queryset=Rental.objects.all(), empty_label="Select Rental")

class BrokerSelectionForm(forms.Form):
    """Form for applicant to select the broker that showed the unit"""
    broker = forms.ModelChoiceField(queryset=Broker.objects.all(), empty_label="Select Broker")

