"""URLs module."""

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', auth_views.login,
        {'template_name': 'hope/signin.html'}, name='signin'),
    url(r'^signout/$', auth_views.logout,
        {'template_name': 'hope/signout.html'}, name='signout'),
    url(r'^account_activation_sent/$',
        TemplateView.as_view(template_name='hope/account_activation_sent.html'),  # noqa
        name='account_activation_sent'),
    url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
]
