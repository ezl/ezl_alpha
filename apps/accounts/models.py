from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
# from django.db.models.signals import post_save

from rentals.models import Rental

USER_TYPES = (
    ("Applicant", "Applicant"),
    ("Broker", "Broker"),
    ("Agency", "Agency"),
    ("Landlord", "Landlord"),
)

# If you want to get fancy, don't define user_types
# In [36]: inspect.getmembers(accounts.models, lambda x: hasattr(x, "user"))
# Out[36]: 
# [('Agency', <class 'accounts.models.Agency'>),
#  ('Applicant', <class 'accounts.models.Applicant'>),
#  ('Broker', <class 'accounts.models.Broker'>),
#  ('Landlord', <class 'accounts.models.Landlord'>),
#  ('UserProfile', <class 'accounts.models.UserProfile'>)]

# use description as a keyword that is the helptext/identifier for the choice in the option
# In [36]: inspect.getmembers(accounts.models, lambda x: hasattr(x, "description"))
# USER_TYPES = tuple([(name, klass.description) for name, klass in object_list])

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User)
    default_view = models.CharField(max_length=255, choices=USER_TYPES,
                                    verbose_name="Whats your user type, sir?")

    def __unicode__(self):
        return '%s: %s' % (self.default_view, self.user)

# TODO: like rz's thinking aobut using signals.  how should leasely be using this?
# def create_profile(sender, instance, **kwargs):
#     if instance is None:
#         return
#     user_profile, created = UserProfile.objects.get_or_create(user=instance)
# post_save.connect(create_profile, sender=User)

class Applicant(TimeStampedModel):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.user)

class Broker(TimeStampedModel):
    user = models.OneToOneField(User)
    agency = models.ForeignKey("Agency", blank=True, null=True)

    # TODO: this may be illegal in IL. confirm with Abe
    # which rentals do they represent?
    rentals = models.ManyToManyField(Rental)
    def __unicode__(self):
        return unicode(self.user)

class Agency(TimeStampedModel):
    user = models.OneToOneField(User)

    # descriptive information about a company
    name = models.CharField(max_length=255, help_text="the name of this real estate agency",
                            blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    zipcode = models.CharField(max_length=255)
    principal = models.CharField(max_length=255, help_text="the owner or principal decision maker of this organization",
                                 blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    alternate_phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)

    # which rentals do they represent?
    rentals = models.ManyToManyField(Rental)
    def __unicode__(self):
        return unicode(self.user)

class Landlord(TimeStampedModel):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.user)
