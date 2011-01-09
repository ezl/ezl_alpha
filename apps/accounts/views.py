from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template

from aplicaciones.models import ApplicationDocument
from accounts.models import UserProfile, Applicant, Broker, Agency, Landlord
from accounts.forms import AgencySettingsForm, UserSettingsForm, UserCreationForm

def common_settings(fn):
    """Decorator to inject settings context that is common to all user_types.

    Each type of user has its own specific settings.  However, instead of 2 settings
    pages (e.g. one for me as the site user, one for me as a broker), jumble all
    this into one settings page.  To get the same shared universal user settings
    forms on each specific user type settings pages, this decorator processes the
    POST data to see if the common informatino was filled out, then injects the common
    context into the specific views.

    As of 10/8/2010 that only includes a form to select the default view for the
    user."""
    def wrapped_view(request):
        user_settings_form = UserSettingsForm(instance=request.user.get_profile())
        if request.POST.has_key("default_view"):
            # they submitted the user settings
            user_settings_form = UserSettingsForm(request.POST, instance=request.user.get_profile())
            if user_settings_form.is_valid():
                user_settings_form.save()
        return fn(request, user_settings_form=user_settings_form)
    return wrapped_view

@login_required
@common_settings
def applicant_settings(request, user_settings_form=None, template='accounts/applicant_settings.html'):
    applicant = Applicant.objects.get(user=request.user)
    application_document_list = ApplicationDocument.objects.filter(applicant=applicant)
    # avoiding generic.object_list because this view will ultimately contain more
    return direct_to_template(request, template, locals())

@login_required
@common_settings
def broker_settings(request, user_settings_form=None, template='accounts/broker_settings.html'):
    broker = Broker.objects.get(user=request.user)
    application_document_list = ApplicationDocument.objects.filter(broker=broker)
    return direct_to_template(request, template, locals())

@login_required
@common_settings
def agency_settings(request, user_settings_form=None, template='accounts/agency_settings.html'):
    agency = Agency.objects.get(user=request.user)
    if request.method == "POST":
        agency_settings_form = AgencySettingsForm(request.POST, instance=agency)
        if agency_settings_form.is_valid():
            agency_settings_form.save()
    if request.method == "GET":
        agency_settings_form = AgencySettingsForm(instance=agency)
    return direct_to_template(request, template, locals())

@login_required
@common_settings
def landlord_settings(request, user_settings_form=None, template='accounts/landlord_settings.html'):
    return direct_to_template(request, template, locals())

@login_required
def settings(request, view=None):
    """Redirect to the user's specific settings.

       The site is designed so that each user has a default user view.
       If the user intends to use the site primarily as a broker, its possible
       that the user will never even know that the other functionality exists.

       Users technically can act in all possible user capacities and thus can also
       set settings as each user type (applicant, broker, agency, landlord).  This
       plain, unspecified "settings" view redirects them to their default view.
    """
    view = request.user.get_profile().default_view
    REDIRECT = {
        "Applicant": "applicant_settings",
        "Broker": "broker_settings",
        "Agency": "agency_settings",
        "Landlord": "landlord_settings",
    }
    return HttpResponseRedirect(reverse(REDIRECT[view]))

def register(request, template='registration/register.html'):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            username = user_creation_form.cleaned_data['username']
            password = user_creation_form.cleaned_data['password1']
            default_view = user_creation_form.cleaned_data['default_view']
            user = user_creation_form.save()
            user = authenticate(username=username, password=password)
            # TODO:
            # i had to assign user twice here.  must authenticate before login,
            # but form doesn't do that.  should really return an authenticated user
            # after user creation
            login(request, user)
            for UserModel in [Applicant, Broker, Agency, Landlord]:
                UserModel.objects.get_or_create(user=user)
            UserProfile.objects.get_or_create(user=user, default_view=default_view)
            messages.info(request, "You have successfully created an account")
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return direct_to_template(request, template, locals())
    user_creation_form = UserCreationForm()
    return direct_to_template(request, template, locals())
