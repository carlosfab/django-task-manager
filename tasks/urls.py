from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('tarefas/', views.task_list, name='task_list'),
    path('tarefas/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tarefas/nova/', views.create_task, name='create_task'),
    path('tarefas/<int:task_id>/editar/', views.update_task, name='update_task'),
    path('tarefas/<int:task_id>/excluir/', views.delete_task, name='delete_task'),
    path('tarefas/<int:task_id>/alternar/', views.toggle_complete, name='toggle_complete'),
    path('tarefas/<int:task_id>/atualizar-bucket/', views.update_task_bucket, name='update_task_bucket'),
]