from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

# from units.models import Unit

class Rental(TimeStampedModel):
    unit = models.ForeignKey("units.Unit")
    creator = models.ForeignKey(User)
    landlord = models.ForeignKey('accounts.Landlord', null=True, blank=True,
                                 help_text="landlord field not required")
    rent_amount = models.FloatField(null=True, blank=True)
    start_date = models.DateField(help_text="when will this rental property available?",
                                  blank=True, null=True)

    def __unicode__(self):
        return 'Unit: %s, Rent: %s, Available: %s' % \
            (self.unit, self.rent_amount, self.start_date)
