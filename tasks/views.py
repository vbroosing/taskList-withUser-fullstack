from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# HOME
def home(req):
    return render(req, 'home.html')

# ADMINISTRACION DE USUARIOS
def signup(req):

    form = UserCreationForm()  # Instanciando el form
    
    if req.method == 'POST':
        if req.POST['password1'] == req.POST['password2']:
            try:
                # registrar Usuario
                user = User.objects.create_user(username=req.POST['username'], password=req.POST['password1'])
                user.save()

                # iniciando sesion
                login(req, user)

                return redirect('tasks') 
            except IntegrityError:
                return render(req, 'signup.html', {
                    'form': form,
                    'error': 'El usuario ya existte',
                })
        else:
            return render(req, 'signup.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden.',
                })
    
    elif req.method == 'GET':
        return render(req, 'signup.html', {'form': form})  # Pasamos el formulario al template

def signin(req):
    form = AuthenticationForm()

    if req.method == 'GET':
        return render(req, 'signin.html', {'form': form})
    else:
        user = authenticate(req, username=req.POST['username'], password=req.POST['password'])
        if user is None:
            return render(req, 'signin.html', {'form': form, 'error': 'Usuario no registrado'})
        else:

            login(req, user)
            return redirect('tasks')

def signout(req):
    logout(req)
    return redirect('home')

# MANEJO DE TAREAS
def tasks(req):
    return render(req, 'tasks.html')

def create_task(req):
    if req.method == 'GET':
        return render(req, 'create-task.html', {'form': TaskForm, })
    else:
        try:
            print(req.POST)
            form = TaskForm(req.POST)
            new_task = form.save(commit=False)
            new_task.user = req.user
            print(new_task)
            new_task.save()
            return redirect('tasks')
        except Exception as e:
            return render(req, 'create-task.html', {
                'form': TaskForm,
                'error': 'Error de tipo: {}'.format(e),
                   })
            