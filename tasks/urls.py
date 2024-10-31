from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),

    # ADMINISTRACION DE USUSARIOS
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),

    # TAREAS
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_task, name='addTask'),

]   