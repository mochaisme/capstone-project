from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class MahasiswaRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 3  # Mahasiswa
        if commit:
            user.save()
        return user

class DosenRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2  # Dosen
        if commit:
            user.save()
        return user
