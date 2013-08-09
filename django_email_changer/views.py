from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic.base import View, TemplateView

from django_email_changer.forms import UserEmailModificationForm
from django_email_changer.models import UserEmailModification


class CreateUserEmailModificationRequest(FormView):
    
    form_class = UserEmailModificationForm
    http_method_names = ["get", "post", ]
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


class ActivateUserEmailModification(TemplateView):

    template_name = "django_email_changer/activate_new_email.html"
    http_method_names = ['get', ]

    def get(self, request, code, *args, **kwargs):
        uem = get_object_or_404(UserEmailModification, security_code=code, user=request.user)
        uem.activate()
        context = self.get_context_data()
        return self.render_to_response(context)
