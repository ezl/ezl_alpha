from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from django.contrib.localflavor.us.forms import USZipCodeField

from accounts.models import UserProfile, Agency

from accounts.models import USER_TYPES

class UserSettingsForm(forms.ModelForm):
    # default_view = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)
    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserCreationForm(AuthUserCreationForm):
    # TODO: multiple inheritance
    # This form should be created like:
    # class UserCreationForm(AuthUserCreationForm, UserSettingsForm):
    #     pass
    label = "In what capacity will you generally be using this site?"
    help_text = '''<p>Select "Applicant" if you will be using the site as a tenant or prospective tenant to apply to live at a rental property.</p>
                   <p>Select "Broker" if you will be an employee or independent agent representing yourself or a real estate brokerage company.</p>
                   <p>Select "Agency" if you are NOT acting in the capacity of a broker, but are part of an organization that manages listings and has realtors as employees.</p>
                   <p>Select "Landlord" if you are the owner or manager of a rental property and have the ability to sign a lease for the property or have decision making power over who will live at the property.</p>
                   '''
    default_view = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect, label=label, help_text=help_text)

class AgencySettingsForm(forms.ModelForm):
    zipcode = USZipCodeField(required=False)

    class Meta:
        model = Agency
        exclude = ('user', 'rentals',)

