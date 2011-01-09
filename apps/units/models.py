from django.db import models
# from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from django.contrib.localflavor.us.models import USStateField

class Unit(TimeStampedModel):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    zipcode = models.CharField(max_length=255)
    # owner = models.ForeignKey(User)
    # creator = models.ForeignKey(User)

    def __unicode__(self):
        return '%s %s, %s, %s %s' % \
            (self.address1, self.address2, self.city, self.state, self.zipcode)
