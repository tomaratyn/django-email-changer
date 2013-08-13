# Copyright 2013 Tom Aratyn <tom@aratyn.name>
#
# This program is licensed under the MIT license (see LICENSE or http://opensource.org/licenses/MIT)
#

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from django_email_changer.views import CreateUserEmailModificationRequest, ActivateUserEmailModification

urlpatterns = patterns('',
                       url(r'^change_email$',
                           login_required(CreateUserEmailModificationRequest.as_view()),
                           name="django_email_changer_change_view"),
                       url(r'activate_email/(?P<code>[^/]+)',
                           login_required(ActivateUserEmailModification.as_view()),
                           name="django_change_email_activate_new_email")
                       )