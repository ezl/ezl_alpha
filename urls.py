from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}, name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'accounts/logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/'}, name='logout'),
    # TODO: no leading ^ on logout?
)

# aplicaciones
urlpatterns += patterns('',
    url(r'^app/(?P<rental_id>\d+)-(?P<broker_id>\d+)/$', 'aplicaciones.views.application', name='application'),
    url(r'^app/(?P<rental_id>\d+)-(?P<broker_id>\d+)/printable/$', 'aplicaciones.views.printable_application', name='printable_application'),
    url(r'^app/start/(?P<rental_id>\d+)-(?P<broker_id>\d+)/$', 'aplicaciones.views.start_application', name='start_application'),
    url(r'^app/edit/(?P<application_document_id>\d+)/$', 'aplicaciones.views.edit_application', name='edit_application'),
    url(r'^app/view/(?P<application_document_id>\d+)/$', 'aplicaciones.views.view_application', name='view_application'),
    # AJAX
    url(r'^app/accept/(?P<application_document_id>\d+)/$', 'aplicaciones.views.accept_application', name='accept_application'),
    url(r'^app/reject/(?P<application_document_id>\d+)/$', 'aplicaciones.views.reject_application', name='reject_application'),
    url(r'^app/remove/(?P<application_document_id>\d+)/$', 'aplicaciones.views.remove_application', name='remove_application'),
    # TODO: Questionable. I do like using http as the primary api though.
    url(r'^app/setpending/(?P<application_document_id>\d+)/$', 'aplicaciones.views.set_application_pending_landlord_decision',
                                                                             name='set_application_pending_landlord_decision'),
)

# rentals
urlpatterns += patterns('',
    url(r'^rental/remove/(?P<rental_id>\d+)/$', 'rentals.views.remove_rental', name='remove_rental'),
)

# dashboard
urlpatterns += patterns('',
    url(r'^dashboard/applicant/$', 'dashboard.views.applicant_dashboard', name='applicant_dashboard'),
    url(r'^dashboard/broker/$', 'dashboard.views.broker_dashboard', name='broker_dashboard'),
    url(r'^dashboard/agency/$', 'dashboard.views.agency_dashboard', name='agency_dashboard'),
    url(r'^dashboard/landlord/$', 'dashboard.views.landlord_dashboard', name='landlord_dashboard'),
    url(r'^dashboard/$', 'dashboard.views.dashboard', name='dashboard'),
)

# accounts
urlpatterns += patterns('',
    url(r'^accounts/register/$', 'accounts.views.register', name='register'),

    url(r'^settings/applicant/$', 'accounts.views.applicant_settings', name='applicant_settings'),
    url(r'^settings/broker/$', 'accounts.views.broker_settings', name='broker_settings'),
    url(r'^settings/agency/$', 'accounts.views.agency_settings', name='agency_settings'),
    url(r'^settings/landlord/$', 'accounts.views.landlord_settings', name='landlord_settings'),
    url(r'^settings/$', 'accounts.views.settings', name='settings'),
)

# developmentgarbage
urlpatterns += patterns('',
    url(r'^unit/update/(?P<unit_id>\d+)/$', 'developmentgarbage.views.update_unit', name='update_unit'),
    url(r'^unit/create/$', 'developmentgarbage.views.create_unit', name='create_unit'),
    url(r'^unit/list/$', 'developmentgarbage.views.list_units', name='list_units'),

    url(r'^rental/update/(?P<rental_id>\d+)/$', 'developmentgarbage.views.update_rental', name='update_rental'),
    url(r'^rental/create/$', 'developmentgarbage.views.create_rental', name='create_rental'),
    url(r'^rental/list/$', 'developmentgarbage.views.list_rentals', name='list_rentals'),

    url(r'^user/list/$', 'developmentgarbage.views.list_users', name='list_users'),
    url(r'^app/list/$', 'developmentgarbage.views.list_application_documents', name='list_application_documents'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^raw_template/(?P<template>.*)', 'django.views.generic.simple.direct_to_template'),
    )

