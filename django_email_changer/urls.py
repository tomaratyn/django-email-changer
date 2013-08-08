from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from django_email_changer.views import CreateUserEmailModificationRequest

urlpatterns = patterns('',
                       url(r'^change_email$',
                           login_required(CreateUserEmailModificationRequest.as_view()),
                           name="django_email_changer_change_view"),
                       )