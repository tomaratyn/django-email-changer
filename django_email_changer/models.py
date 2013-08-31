# Copyright 2013 Tom Aratyn <tom@aratyn.name>
#
# This program is licensed under the MIT license (see LICENSE or http://opensource.org/licenses/MIT)
#

from datetime import timedelta
from string import translate
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from django_email_changer import settings


def create_security_code():
    return translate(str(uuid4()), None, "-")


class UserEmailModification(models.Model):

    user = models.ForeignKey(User, blank=False, null=False)
    new_email = models.EmailField(max_length=255, blank=False)
    security_code = models.CharField(max_length=33, default=create_security_code, blank=False)
    date_change_proposed = models.DateTimeField(auto_now_add=True)
    date_change_accepted = models.DateTimeField(blank=True, null=True)

    def activate(self):
        """
        returns true if we activate the new email, false otherwise.
        """
        expiry_datetime = now() - timedelta(**settings.CHANGE_EMAIL_CODE_EXPIRY_TIME)
        if expiry_datetime < self.date_change_proposed and self.date_change_accepted is None:
            self.user.email = self.new_email
            self.user.save()
            self.date_change_accepted = now()
            self.save()
            return True
        return False

