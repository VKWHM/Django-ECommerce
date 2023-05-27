from django import forms

from .models import UserBase


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Enter User Name", min_length=4, max_length=30, help_text="Required")
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required':'Sorray, you will need an email'}, label="Enter Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('username', 'email',)

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username'].lower()
        rows = UserBase.objects.filter(username = username)
        if rows.count():
            raise forms.ValidationError("Username already Exists")
        return username

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data['email']
        rows = UserBase.objects.filter(email = email)
        if rows.count():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email

    def clean_repeat_password(self, *args, **kwargs):
        pass1, pass2 = self.cleaned_data['password'], self.cleaned_data['repeat_password']
        if pass1 != pass2:
            raise forms.ValidationError("Passwords do not match.")
        return pass1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'email', 'password', 'repeat_password']:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': self.fields[field].label or ''})
