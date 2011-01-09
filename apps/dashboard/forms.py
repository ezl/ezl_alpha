from django import forms

from units.forms import UnitCreationForm

class UnitAndRentalCreationForm(UnitCreationForm):
    # TODO: multiple inheritance
    # class UnitAndRentalCreationForm(UnitCreationForm, RentalCreationForm)
    #     pass
    # http://code.djangoproject.com/ticket/7018

    from accounts.models import Landlord
    # TODO:import here because ths class will disappear once the correct landlord
    # entry method is in place
    landlord = forms.ModelChoiceField(queryset=Landlord.objects.all(),
                                      required=False,
                                      help_text="landlord field is not required")
    # TODO: better way to get the landlord in here.
    # 2 approaches:
    # 1. just an email address so he can keep getting notifications
    # 2. create a temp account and send landlord something to register to claim it
    rent_amount = forms.DecimalField(required=False)
    # TODO: sort out DecimalField vs FloatField
    start_date = forms.DateField(required=False)

class BrokerAdoptionForm(forms.Form):
    """An agency representative can use this form to add a broker to their roster"""
    from accounts.models import Broker
    # TODO:import here because ths class will disappear once the correct broker
    # adoption method is in place
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    broker = forms.ModelChoiceField(queryset=Broker.objects.all(), empty_label="select a Broker")
