from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import (create_object,
                                                update_object,
                                                delete_object)
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from accounts.models import UserProfile
from rentals.models import Rental
from units.models import Unit
from aplicaciones.models import ApplicationDocument
from units.forms import UnitCreationForm
from rentals.forms import RentalCreationForm

""" GARBAGE HELPER VIEWS DURING DEVELOPMENT """

def list_application_documents(request, template='developmentgarbage/list_application_documents.html'):
    qs = ApplicationDocument.objects.all()
    return object_list(request, queryset=qs, template_name=template)

def list_users(request, template='developmentgarbage/list_users.html'):
    qs = User.objects.all()
    return object_list(request, queryset=qs, template_name=template)

def list_rentals(request, template='developmentgarbage/list_objects.html'):
    qs = Rental.objects.all()
    return object_list(request, queryset=qs, template_name=template)

def list_units(request, template='developmentgarbage/list_objects.html'):
    qs = Unit.objects.all()
    return object_list(request, queryset=qs, template_name=template)

def create_unit(request, template='developmentgarbage/create_modify_object.html'):
    return create_object(request, form_class=UnitCreationForm, template_name=template,
                             post_save_redirect=reverse('home'))

def update_unit(request, unit_id=None, template='developmentgarbage/create_modify_object.html'):
    unit_id_exists = True if Unit.objects.filter(id=unit_id) else False
    if unit_id_exists:
        return update_object(request, form_class=UnitCreationForm, object_id=unit_id,
                             template_name=template,
                             post_save_redirect=reverse('home'))
    else:
        messages.info(request, "Leasely couldn't find the unit you're looking for. Do you want to create it?")
        return HttpResponseRedirect(reverse(create_unit))

@login_required
def create_rental(request, template='developmentgarbage/create_modify_object.html'):
    form = RentalCreationForm()
    if request.method == "POST":
        form = RentalCreationForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.creator = request.user
            rental.save()
            messages.info("The rental was successfully created.")
    return direct_to_template(request, template, locals())

def update_rental(request, rental_id=None, template='developmentgarbage/create_modify_object.html'):
    rental_id_exists = True if Rental.objects.filter(id=rental_id) else False
    if rental_id_exists:
        return update_object(request, form_class=RentalCreationForm, object_id=rental_id,
                             template_name=template,
                             post_save_redirect=reverse('home'))
    else:
        messages.info(request, "Leasely couldn't find the rental you're looking for. Do you want to create it?")
        return HttpResponseRedirect(reverse(create_rental))

