from django.urls import path

from .views import (LoginPage, RegistrationPage, account_activate,
                    account_dashboard)

app_name = 'account'

urlpatterns = [
    path('register/', RegistrationPage.as_view(), name="registration_page"),
    path('login/', LoginPage.as_view(), name="login_page"),
    path('dashboard/', account_dashboard, name="dashboard_page"),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name="activate_page")
]
