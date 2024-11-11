from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def signout(req):
    logout(req)
    return redirect('home')

# MANEJO DE TAREAS
@login_required
def tasks(req):
    if req.user.username == 'michel':

        all_tasks = Task.objects.filter(date_completed__isnull=True)
    else:
        all_tasks = Task.objects.filter(user=req.user, date_completed__isnull=True)

    # print(all_tasks)
    return render(req, 'tasks.html', {'tasks': all_tasks})

@login_required
def complete_tasks(req):

    if req.user.username == 'michel':
        all_tasks = Task.objects.filter(date_completed__isnull=False)
    else:
        all_tasks = Task.objects.filter(user=req.user, date_completed__isnull=False).order_by('-date_completed')

    return render(req, 'tasks_completed.html', {'tasks': all_tasks})

@login_required
def create_task(req):

    if req.user:
        if req.method == 'GET':
            return render(req, 'create-task.html', {'form': TaskForm, })
            
        else:
            try:
                # print(req.POST)
                form = TaskForm(req.POST)
                new_task = form.save(commit=False)
                new_task.user = req.user
                # print(new_task)
                new_task.save()
                return redirect('tasks')
            except Exception as e:
                return render(req, 'create-task.html', {
                    'form': TaskForm,
                    'error': 'Error de tipo: {}'.format(e),
                    })
    else:
        if req.method == 'GET':
            return render(req, 'home.html', {
                'error': 'Error de tipo: {}'.format(e),
                })
        else:
            return render(req, 'home.html', {
                'form': TaskForm, 
                'error': 'Debes Iniciar sesión para añadir una tarea'
                })

@login_required           
def task_detail(req, task_id):

    if req.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=req.user)
        form = TaskForm(instance=task)
        print(task_id)
        return render(req, 'task_detail.html', {
            'task': task,
            'form': form,
            })
    else:
        print(req.POST)
        task = get_object_or_404(Task, pk=task_id, user=req.user)
        form = TaskForm(req.POST, instance=task)
        try:
            form.save()
        except ValueError:
            return render(req, 'task_detail.html',{
                'task': task,
                'form': form,
                'error': 'Error actualizando tarea.'
                })

        return redirect('tasks')

@login_required    
def complete_task(req, task_id):
    task = get_object_or_404(Task, pk=task_id, user=req.user)

    if req.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(req, task_id):
    if req.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=req.user)
        task.delete()
        return redirect('tasks')

@login_required
def delete_complete_task(req, task_id):
    if req.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=req.user)
        task.delete()
        return redirect('complete_tasks')

@login_required
def task_complete_detail(req, task_id):
    if req.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=req.user)
        return render(req, 'task_complete_detail.html', {
            'task': task,
            })
    else:
        print(req.POST)
        task = get_object_or_404(Task, pk=task_id, user=req.user)
        form = TaskForm(req.POST, instance=task)
        try:
            form.save()
        except ValueError:
            return render(req, 'task_complete_detail.html',{
                'task': task,
                'form': form,
                'error': 'Error actualizando tarea.'
                })

        return redirect('tasks')