from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template

from aplicaciones.models import ApplicationDocument
from accounts.models import Applicant, Broker, Agency, Landlord
from rentals.models import Rental
from dashboard.forms import UnitAndRentalCreationForm, BrokerAdoptionForm

@login_required
def applicant_dashboard(request, template='dashboard/applicant_dashboard.html'):
    applicant = Applicant.objects.get(user=request.user)
    application_document_list = ApplicationDocument.objects.filter(applicant=applicant)
    # avoiding generic.object_list because this view will ultimately contain more
    return direct_to_template(request, template, locals())

@login_required
def broker_dashboard(request, template='dashboard/broker_dashboard.html'):
    broker = Broker.objects.get(user=request.user)
    unit_and_rental_creation_form = UnitAndRentalCreationForm()
    # broker_rental_list is the list of rentals the broker has added himself.
    # this is independent of the set that his agency represents
    # the agency can't see broker.rentals, but the agency can see
    # ANY application document that his brokers have started, even outside
    # the agency/  is this a problem?
    # agency rental list is the list that his affiliated agency represents
    # its assumed he has access to all of the agency represented rentals

    #broker.agency.rentals.add(rental)
    if request.method == "POST":
        if request.POST.has_key("address1") and request.POST.has_key("rent_amount"):
            unit_and_rental_creation_form = UnitAndRentalCreationForm(request.POST)
            if unit_and_rental_creation_form.is_valid():
                _cleaned_data = unit_and_rental_creation_form.cleaned_data
                rent_amount = _cleaned_data['rent_amount']
                start_date = _cleaned_data['start_date']
                landlord = _cleaned_data['landlord']
                # TODO: save method only saves the Unit (non multiple inheritance)
                # see models
                unit = unit_and_rental_creation_form.save()
                rental = Rental(unit=unit, creator=request.user,
                               rent_amount=rent_amount, start_date=start_date)
                if landlord:
                    rental.landlord = landlord
                rental.save()
                if broker.agency:
                    broker.agency.rentals.add(rental)
                    messages.info(request, "You successfully added a rental unit for your agency")
                else:
                    broker.rentals.add(rental)
                    messages.info(request, "You are not currently affiliated with an agency on Leasely.com.  This rental unit has been added to your personal broker dashboard to track.")
                HttpResponseRedirect(reverse("broker_dashboard"))

    application_document_list = ApplicationDocument.objects.filter(broker=broker)
    return direct_to_template(request, template, locals())

@login_required
def agency_dashboard(request, template='dashboard/agency_dashboard.html'):
    agency = Agency.objects.get(user=request.user)
    broker_adoption_form = BrokerAdoptionForm()

    if request.method == "POST":
        # broker adoption form
        if request.POST.has_key("broker"):
            broker_adoption_form = BrokerAdoptionForm(request.POST)
            if broker_adoption_form.is_valid():
                broker = broker_adoption_form.cleaned_data['broker']
                broker.agency = agency
                broker.save()
                messages.info(request, "broker %s was successfully added to your agency roster" % broker)

    broker_list = Broker.objects.filter(agency=agency)
    rental_list = agency.rentals.all()
    application_document_list = ApplicationDocument.objects.filter(rental__in=rental_list)
    return direct_to_template(request, template, locals())

@login_required
def landlord_dashboard(request, template='dashboard/landlord_dashboard.html'):
    landlord = Landlord.objects.get(user=request.user)
    rentals = Rental.objects.filter(landlord=landlord)
    application_document_list = ApplicationDocument.objects.filter(rental__in=rentals)
    return direct_to_template(request, template, locals())

@login_required
def dashboard(request, view=None):
    """Redirect to the user's specific dashboard.

       The site is designed so that each user has a default user view.
       If the user intends to use the site primarily as a broker, its possible
       that the user will never even know that the other functionality exists.

       Users technically can act in all possible user capacities and thus can also
       set settings as each user type (applicant, broker, agency, landlord).  This
       plain, unspecified "dashboard" view redirects them to their default view.

       We may consider changing this to whatever user_type view they were on last.
    """
    view = request.user.get_profile().default_view
    REDIRECT = {
        "Applicant": "applicant_dashboard",
        "Broker": "broker_dashboard",
        "Agency": "agency_dashboard",
        "Landlord": "landlord_dashboard",
    }
    return HttpResponseRedirect(reverse(REDIRECT[view]))

