from datetime import datetime
from string import translate
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


def create_security_code():
    return translate(str(uuid4()), None, "-")


class UserEmailModification(models.Model):

    user = models.ForeignKey(User, blank=False, null=False)
    new_email = models.EmailField(max_length=255, blank=False)
    security_code = models.CharField(max_length=33, default=create_security_code, blank=False)
    date_change_proposed = models.DateField(auto_now_add=True)
    date_change_accepted = models.DateField(blank=True, null=True)

    def activate(self):
        self.user.email = self.new_email
        self.user.save()
        self.date_change_accepted = datetime.utcnow()

