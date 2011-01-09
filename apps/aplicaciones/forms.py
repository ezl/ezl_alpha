from django import forms
from django.contrib.localflavor.us.forms import (USPhoneNumberField,
                                                 USZipCodeField,
                                                 USSocialSecurityNumberField)

from aplicaciones.models import ApplicationDocument

class ApplicationDocumentForm(forms.ModelForm):
    ssn = USSocialSecurityNumberField(required=False)
    phone = USPhoneNumberField(required=False)
    alternate_phone = USPhoneNumberField(required=False)
    zipcode = USZipCodeField(required=False)
    landlord_phone = USPhoneNumberField(required=False)
    supervisor_phone = USPhoneNumberField(required=False)

    class Meta:
        model = ApplicationDocument
        exclude = ('broker', 'rental', 'applicant', 'status',)
