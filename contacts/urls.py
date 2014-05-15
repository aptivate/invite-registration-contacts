from django.conf.urls import patterns, url
from .views import (
    AddContact, UpdateContact, DeleteContact, ListContacts,
    UpdatePersonalInfo, ListContactsExport
)
from registration.views import SendActivationEmailView


urlpatterns = patterns('',
    url(r'edit/$', AddContact.as_view(), name='contact_add'),
    url(r'edit/(?P<pk>\d+)/$', UpdateContact.as_view(),
        name='contact_update'),
    url(r'delete/(?P<pk>\d+)/$', DeleteContact.as_view(),
        name='contact_delete'),
    url(r'activate/(?P<pk>\d+)/$',
        SendActivationEmailView.as_view(reverse_name='contact_list'),
        name='contact_claim_account'),
    url(r'personal/$', UpdatePersonalInfo.as_view(), name='personal_edit'),
    url(r'export_as_csv/$', ListContactsExport.as_view(), {'format': 'csv'},
        name='contact_list_csv'),
    url(r'export_as_excel/$', ListContactsExport.as_view(), {'format': 'excel'},
        name='contact_list_excel'),
    url(r'$', ListContacts.as_view(), name='contact_list'),

)