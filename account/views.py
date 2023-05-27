from django.urls import reverse
from .forms import RegistrationForm
from django.views import View
from django.shortcuts import render, redirect

class LoginPage(View):
    """docstring for LoginPageView."""
    def get(self,request):
        pass


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
        return render(request, 'account/register.html', {'form': formset})
