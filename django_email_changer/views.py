from django.conf import settings
from django.views.generic import FormView

from django_email_changer.forms import UserEmailModificationForm
from django_email_changer.models import UserEmailModification


class CreateUserEmailModificationRequest(FormView):
    
    form_class = UserEmailModificationForm
    success_url = settings.EMAIL_CHANGE_SUCCESS_URL
    template_name = "django_email_changer/change_email_form.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data.get("password")):
                form.errors["password"] = [u'Wrong password.']
                return self.form_invalid(form)
            new_email = form.cleaned_data.get("new_email")
            UserEmailModification.objects.create(user=request.user, new_email=new_email)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)