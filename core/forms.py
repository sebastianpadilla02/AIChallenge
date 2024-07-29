from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Seller

from BackEnd.App import aplicacion

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Escriba Nombre de Usuario',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Escriba su contraseña',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'direction', 'phone', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Escriba Nombre de Usuario',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Escriba su correo electrónico',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    direction = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Escriba la dirección donde vive',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Digite su número de celular',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Escriba su contraseña',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita su contraseña',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
class SignupSellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ('horario', 'contacto', 'instagram')
    
        horario = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Escriba su Horario de Disponibilidad',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
        contacto = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Escriba su Número de Teléfono',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
        instagram = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Escriba su Cuenta de Instagram',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))