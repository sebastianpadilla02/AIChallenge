import traceback
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import SignupForm, LoginForm, SignupSellerForm
from django.core.files.storage import FileSystemStorage

import os

from BackEnd.App import aplicacion
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

texto_AI = "PRUEBA"

def index(request):
    print(request.user)

    return render(request, 'core/index.html')

@csrf_exempt
def respond_chat (request):
    print("RESPOND CHAT")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', None)
            
            print(texto)
            
            global texto_AI
            texto_AI = aplicacion.obtenerRespuesta(texto)
            print(f"Respuesta: {texto_AI}")
            
            # Procesa la variable como necesites
            response = redirect('/respond_view/')
            print("ERROR CRITICO")
            return response
        except Exception as e:
            traceback.print_exc()
            return redirect('/respond_view/')
    print("ERROR FINAL")
    return redirect('/respond_view/')

def chat (request):
    if request.method == 'POST':
        return redirect('/chat/')
    else:
        return render(request, 'core/chat.html', {
    })

def respond_view (request):
    # Renderiza la plantilla 'respond_view.html'
    print(f"TEXTO A IMPRIMIR {texto_AI}")
    return render(request, 'core/respond_view.html', {'message': texto_AI})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password']
            
            auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm)

            return redirect('/chat/')
    else:
        
        form = LoginForm()

    return render(request, 'core/login.html', {
        'form': form
    })
    
def logout_user(request):
    logout(request)
    print("USUARIO CERRADO")
    return redirect('/login/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            print('Iniciando Registro de Usuario')
            aplicacion.registrarUsuario(username, email, password1, password2)

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })
