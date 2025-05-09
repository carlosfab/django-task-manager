# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.
def home(request):
	title = "Task Manager"
	# Option 1: return a simple string
	# return HttpResponse("Hello, world! This is the home page.")

	# Option 2: return a template
	return render(request, 'tasks/home.html', {
		'title': title,
		'message': 'Welcome to the Task Manager application!'
	})

def task_list(request):
    tasks = Task.objects.order_by('-priority', 'due_date')
    context = {'tasks': tasks}
    return render(request, 'tasks/task_list_kanban.html', context)

# create task_detail, create_task, update_task, delete_task, and toggle_complete views in views.py (empty functions for now)
def task_detail(request, task_id):
	task = Task.objects.get(id=task_id)
	context = {'task': task}
	return render(request, 'tasks/task_detail.html', context)

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Nova Tarefa'})

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {
        'form': form, 
        'title': 'Editar Tarefa'
    })

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarefa excluída com sucesso!')
        return redirect('tasks:task_list')
    
    return render(request, 'tasks/delete_task.html', {'task': task})

def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        
        status_message = 'concluída' if task.completed else 'pendente'
        messages.success(request, f'Tarefa marcada como {status_message}!')
        
        # Check where the request came from to redirect back there
        referer = request.META.get('HTTP_REFERER', '')
        
        if 'task_detail' in referer:
            return redirect('tasks:task_detail', task_id=task.id)
        else:
            return redirect('tasks:task_list')
    
    # In case someone tries to access this URL directly via GET
    return redirect('tasks:task_detail', task_id=task.id)

