from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField

from accounts.models import Applicant, Broker #, Agency, Landlord
from rentals.models import Rental

STATUS_CHOICES = (
    ("INCOMPLETE", "Incomplete."),
    ("COMPLETE", "Complete, but not yet submitted."),
    ("SUBMITTED", "Submitted."), # whats the difference between submitted and pending landlord review? probably none.
    ("PURGATORY", "Leasely has received the request, but has not yet sent it to the landlord.  We may be waiting for the results of the credit/background check to complile the full report to send to the landlord."),
    ("PENDING LANDLORD REVIEW", "The application is available for landlord the landlord, but he has not yet logged in to see the application."),
    ("PENDING LANDLORD DECISION", "The landlord has seen/reviewed the application. We are waiting for him to render a decision."),
    ("ACCEPTED", "The landlord has accepted the application. You should receive a lease to sign."),
    ("REJECTED", "The landlord has rejected your application."),
)

class ApplicationDocument(TimeStampedModel):
    # internal tracking information
    rental = models.ForeignKey(Rental)
    broker = models.ForeignKey(Broker, related_name='applications_managed')
    applicant = models.ForeignKey(Applicant, related_name='applications')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="INCOMPLETE")

    # identity
    first_name = models.CharField(max_length=255, verbose_name="first name")
    middle_name = models.CharField(max_length=255, verbose_name="middle name",
                                   blank=True, null=True)
    last_name = models.CharField(max_length=255, verbose_name="last name",
                                 blank=True, null=True)
    ssn = models.CharField(max_length=255, verbose_name="social security number",
                           blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # contact
    phone = models.CharField(max_length=255, blank=True, null=True)
    alternate_phone = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    # residence
    address1 = models.CharField(max_length=255,
                                verbose_name="current address line 1",
                                help_text="street address, P.O. box, company, c/o",
                                blank=True, null=True)
    address2 = models.CharField(max_length=255,
                                verbose_name="current address line 2",
                                help_text="apartment, suite, unit, building, floor, etc.",
                                blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    landlord_name = models.CharField(max_length=255, blank=True, null=True)
    landlord_phone = models.CharField(max_length=255, blank=True, null=True)
    landlord_email = models.EmailField(blank=True, null=True)

    # employment
    occupation = models.CharField(max_length=255, blank=True, null=True)
    employer = models.CharField(max_length=255, blank=True, null=True)
    supervisor_name = models.CharField(max_length=255, blank=True, null=True)
    supervisor_phone = models.CharField(max_length=255, blank=True, null=True)
    income = models.FloatField(verbose_name="primary income",
                               help_text="how much money you make per year from your primary income source (job, benefits, etc.)?",
                               blank=True, null=True)
    income2 = models.FloatField(verbose_name="additional income",
                               help_text="how much money you make per year from any additional income streams?",
                                blank=True, null=True)

    """I hearby authorize Leasely.com, a credit (consumer?) reporting agency, to charge the above credit card a non-refundable fee
       of $XX.XX in accordance with the terms of my cardholder statement.

       The authorized fee includes an optional $15.00 per applicant for a criminal records check.  If the landlord electts not to run this check,
       your card will be charged $25.00 per applicant instead of the authorized amount.  You will be e-mailed a receipt confirming the actual
       amount charged.

       I hearby apply to lease an apartment and agree that the rental is to be payable the 1st day of each month in advance. I warrant that all statements above set forth are true.

       I hearby give my permission to communicate with my current and former landlord or property manage for the purpose of discussing any and all of the facts and circumstances of my current or former tenancy, as well as the other information listed above.  I also give my permission to communicate with my current employer(s) and/or supervisor(s) for the purpose of verifying the employment information listed above.  I understand there are no limitations or restrictions regarding what may be discussed or revealed.  I am aware that a credit history, eviction search and criminal background check will be done in conjunction with my application.  I understand that I may have the right to make a written request within a reasonable period of time to receive additional, detailed information about the nature and scope of this investigation.

       (I hearby authorize leasely to run the CREDITASD CHECK AND ALL THAT BS)
       """

    # background
    bankruptcy = models.BooleanField(verbose_name="Have you ever filed for  bankruptcy?")
    rent = models.BooleanField(verbose_name = "Have you ever willfully refused to pay rent when due?")
    eviction = models.BooleanField(verbose_name="Have you ever been evicted from a tenancy or left owing money?")
    crime = models.BooleanField(verbose_name="Have you ever been convicted of a crime?")

    # extra
    extra = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return '%s, broker: %s tenant: %s' % \
            (self.rental, self.broker, self.applicant)
