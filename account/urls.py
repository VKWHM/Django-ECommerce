from django.urls import path
from .views import RegistrationPage
from .views import LoginPage

app_name = 'account'

urlpatterns = [
    path('register/', RegistrationPage.as_view(), name="registration_page"),
    path('login/', LoginPage.as_view(), name="login_page"),
]
