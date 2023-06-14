from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import RegistrationForm
from .models import UserBase
from .token import AccountActivationTokenGenerator


@login_required()
def account_dashboard(request, *args, **kwargs):
    return render(request, 'account/dashboard.html')

def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = UserBase.objects.get(pk=uid)
    except Exception as e:
        pass
    else:
        if user is not None and AccountActivationTokenGenerator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('account:dashboard_page'))
    return redirect('/')

class RegistrationPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('account:dashboard_page'))
        formset = RegistrationForm()
        return render(request, 'account/register.html', {'form': formset})

    def post(self, request):
        formset = RegistrationForm(request.POST)
        if formset.is_valid():
            user = formset.save(commit=False)
            user.email = formset.cleaned_data['email']
            user.set_password(formset.cleaned_data['repeat_password'])
            user.is_active = False
            user.save()
            subject = "Activate Your Account"
            message = render_to_string('account/account_activation_message.html', {
                "username": user.username,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": AccountActivationTokenGenerator.make_token(user)
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse("You're Registred Successfully.")
        return render(request, 'account/register.html', {'form': formset})
