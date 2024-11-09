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
    path('tasks_completed/', views.complete_tasks, name='complete_tasks'),
    path('tasks/create/', views.create_task, name='addTask'),
    path('tasks/<int:task_id>/', views.task_detail, name='taskDetail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),

]   