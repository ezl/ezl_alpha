from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

from aplicaciones.models import ApplicationDocument
from rentals.models import Rental
from accounts.models import Applicant, Broker

from aplicaciones.forms import ApplicationDocumentForm
from developmentgarbage.forms import RentalSelectionForm, BrokerSelectionForm

# AJAX requests -- TODO there is currently NO SECURITY on these AJAX calls

def accept_application(request, application_document_id=None):
    return set_application_status(request, application_document_id, "ACCEPTED")

def reject_application(request, application_document_id=None):
    return set_application_status(request, application_document_id, "REJECTED")

def set_application_pending_landlord_decision(request, application_document_id=None):
    return set_application_status(request, application_document_id, "AWAITING LANDLORD DECISION")

def remove_application(request, application_document_id=None):
    """Remove application document from dashboard.

       This view is currently bunko, it just straight up deletes the record.  We
       should never delete these records? and we should just remove it from THAT
       user's view. Yay more model fields.  TODO: (for project grepping)"""
    try:
        application_document = ApplicationDocument.objects.get(id=application_document_id)
        application_document.delete()
    except:
        return HttpResponse("Fail")
    else:
        return HttpResponse("Success")

# AJAX helpers

def set_application_status(request, application_document_id=None, status=None):
    try:
        application_document = ApplicationDocument.objects.get(id=application_document_id)
        application_document.status = status
        application_document.save()
    except:
        return HttpResponse("Fail")
    else:
        return HttpResponse("Success")

# "Normal" views
def printable_application(request, rental_id=None, broker_id=None):
    return application(request, rental_id=rental_id, broker_id=broker_id, printable=True)

def application(request, rental_id=None, broker_id=None, printable=False, \
                template='aplicaciones/application.html'):
    """ApplicationDocuments are created in this view.

       Only use case is an applicant filling out a form to apply.
       This page should be the first point of contact for most tenants -- a
       broker gives the applicant a URL and they land here.
    """
    try:
        rental = Rental.objects.get(id=rental_id)
    except Rental.DoesNotExist:
        rental = None
    try:
        broker = Broker.objects.get(id=broker_id)
    except Broker.DoesNotExist:
        broker = None
    if not rental or not broker:
        # as per discussion with rz, this action will probably
        # be different later
        return HttpResponseRedirect(reverse("start_application",
                                    kwargs={'rental_id': rental_id,
                                            'broker_id': broker_id}))

    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse("You must log in to save or submit.")
        application_document_form = ApplicationDocumentForm(request.POST)
        if application_document_form.is_valid():
            application_document = application_document_form.save(commit=False)
            application_document.applicant = Applicant.objects.get(user=request.user)
            application_document.broker = broker
            application_document.rental = rental
            application_document.save()
            if request.POST['submit'] == "Submit to landlord":
            # TODO: DRY. hardcoding "submit to landlord" text comparison will break if we change
            # the button value in the template.  Also I just copied this logic from the edit_application view.
                """point here is to change the status flag if we submit to landlord"""
                application_document.status = "SUBMITTED"
                application_document.save()
                messages.info(request, "Your application has been submitted.  You can track your application status through your dashboard.")
                return HttpResponseRedirect(reverse("dashboard"))
            else: # the applicant saved, but didn't submit
                messages.info(request, "Your application was successfully saved.  You can continue to edit or [return to your dashboard].")
                return HttpResponseRedirect(reverse("edit_application",
                                             kwargs={'application_document_id': \
                                                     application_document.id}))
        else:
            return direct_to_template(request, template, locals())

    if request.method == 'GET':
        if not request.user.is_authenticated():
            messages.info(request, """You must be logged in to save or submit a rental application.  Please [log in] or [sign up].  [Click here] to learn more about Leasely before making a decision or check out the sidebar for a short summary of the benefits you'll receive by joining Leasely.""")
        application_document_form = ApplicationDocumentForm()
        return direct_to_template(request, template, locals())

@login_required
def edit_application(request, application_document_id=None, template='aplicaciones/application.html'):
    # all these application things ought likely be combined into a smaller number of views
    application_document = get_object_or_404(ApplicationDocument, id=application_document_id)

    # submitted applications can't be edited anymore, redirect to the view page
    if not application_document.status == "INCOMPLETE":
        return view_application(request, application_document_id=application_document_id)

    if not application_document.applicant.user == request.user:
        # TODO: what should we do if the user doesn't have permission to access this page?
        return HttpResponse("You do not have permission to edit this application.")
    application_document_form = ApplicationDocumentForm(instance=application_document)
    broker = application_document.broker
    applicant = application_document.applicant
    rental = application_document.rental

    if request.method == "POST":
        application_document_form = ApplicationDocumentForm(request.POST, instance=application_document)
        if application_document_form.is_valid():
            application_document_form.save()
            if request.POST['submit'] == "Submit to landlord":
            # TODO: DRY. hardcoding "submit to landlord" text comparison will break if we change
            # the button value in the template.
                """point here is to change the status flag if we submit to landlord"""
                application_document.status = "SUBMITTED"
                application_document.save()
                messages.info(request, "Your application has been submitted.  You can track your application status through your dashboard.")
                return HttpResponseRedirect(reverse("dashboard"))
    return direct_to_template(request, template, locals())

@login_required
def view_application(request, application_document_id=None, template='aplicaciones/view_application.html'):
    """View an application document.

       View but not edit an application.  For now anyone can see it.  Who should we restrict this
       to?
    """
    # all these application things ought likely be combined into a smaller number of views
    application_document = get_object_or_404(ApplicationDocument, id=application_document_id)
    # if not request.user in authorized_viewers:
    #     # TODO: what should we do if the user doesn't have permission to access this page?
    #     return HttpResponse("You do not have permission to edit this application.")
    application_document_form = ApplicationDocumentForm(instance=application_document)
    broker = application_document.broker
    applicant = application_document.applicant
    rental = application_document.rental
    messages.info(request, "this form looks editable but its not. it should eventually be a form to display the contents in a nice manner for users who can not edit it (or after submission, when the applicant can no longer submit)")
    # TODO: pooper scooper.  i can't display the form field.value in the template!
    # a = application_document_form
    # first = a['first_name']
    # ff = first.field
    # raise Exception

    return direct_to_template(request, template, locals())

def start_application(request, rental_id=None, broker_id=None, template='aplicaciones/start_application.html'):
    """Set the ApplicationDocuments relevant viewers/participants.

       ApplicationDocuments require a rental and broker id.  That data is not
       set in the actual application (don't want users setting it), so this view sets them.

       After discussion, it seems that we may not want this functionality to exist on "bad hash"
       scenarios, so we might change this to only exist for tenants/landlors creating a new application,
       then redirecting somewhere else.

       Currently, you choose rentals/brokers from a drop down.  That funcitonality won't exist -- you'll
       either create them/invite brokers to use Leasely, then the filled out ap will be sent to the person.
       Only authenticated users should be able to do this?"""

    # last remnants of the RentalSelectionForm.  when this is removed,
    # remove it from the imports
    try:
        rental = Rental.objects.get(id=rental_id)
    except Rental.DoesNotExist:
        rental = None
        rental_selection_form = RentalSelectionForm()
    try:
        broker = Broker.objects.get(id=broker_id)
    except Broker.DoesNotExist:
        broker = None
        broker_selection_form = BrokerSelectionForm()

    if request.method == "POST":
        rental_selection_form = RentalSelectionForm(request.POST)
        broker_selection_form = BrokerSelectionForm(request.POST)
        if rental_selection_form.is_valid():
            rental = rental_selection_form.cleaned_data['rental']
        if broker_selection_form.is_valid():
            broker = broker_selection_form.cleaned_data['broker']
        if rental and not broker:
            return HttpResponseRedirect(reverse("start_application", kwargs={'rental_id': rental.id, 'broker_id': broker_id}))
        if broker and not rental:
            return HttpResponseRedirect(reverse("start_application", kwargs={'rental_id': rental_id, 'broker_id': broker.id}))

    if rental and broker:
        return HttpResponseRedirect(reverse("application", kwargs={'rental_id': rental.id, 'broker_id': broker.id}))
    if not rental:
        messages.info(request, "Sorry, we couldn't find the rental for that lease. Please see if its in our list.")
    if not broker:
        messages.info(request, "Sorry, we couldn't find the broker you specified. See if he/she is listed below.")

    return direct_to_template(request, template, locals())
