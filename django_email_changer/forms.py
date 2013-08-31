# Copyright 2013 Tom Aratyn <tom@aratyn.name>
#
# This program is licensed under the MIT license (see LICENSE or http://opensource.org/licenses/MIT)
#

from django import forms
from django.forms.models import ModelForm

from django_email_changer.models import UserEmailModification


class UserEmailModificationForm(ModelForm):
    class Meta:
        model = UserEmailModification
        fields = ("new_email", )

    confirmed_email = forms.EmailField(required=True, label="Confirm Email")
    password = forms.CharField(required=True, label="Your Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(UserEmailModificationForm, self).clean()
        new_email = cleaned_data.get("new_email")
        confirmed_email = cleaned_data.get("confirmed_email")
        if new_email == confirmed_email:
            return cleaned_data
        else:
            raise forms.ValidationError("Please provide the email and the confirmed email.")
