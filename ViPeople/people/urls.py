from django.conf.urls import patterns, include, url

from .views import ListPeople, CreatePeople, UpdatePeople, DeletePeople

urlpatterns = patterns('',
    url(r'^$', ListPeople.as_view(), name='people_list'),
    url(r'^peoples/create/$', CreatePeople.as_view(), name='people_create'),
    url(r'^peoples/(?P<pk>\d+)/$', UpdatePeople.as_view(), name='people_view'),
    url(r'^peoples/(?P<pk>\d+)/update/$', UpdatePeople.as_view(), name='people_update'),
    url(r'^peoples/(?P<pk>\d+)/delete/$', DeletePeople.as_view(), name='people_delete'),
)