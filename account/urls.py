from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.base import reverse_lazy

from .forms import UserLoginForm
from .views import RegistrationPage, account_activate, account_dashboard

app_name = 'account'

urlpatterns = [
    path('register/', RegistrationPage.as_view(), name="registration_page"),
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm, template_name="account/login.html"), name="login_page"),
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("account:login_page")), name="logout_page"),
    path('dashboard/', account_dashboard, name="dashboard_page"),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name="activate_page")
]
