# from django.http import HttpResponse
from django.shortcuts import render
from .models import Task

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
    return render(request, 'tasks/task_list.html', context)

# create task_detail, create_task, update_task, delete_task, and toggle_complete views in views.py (empty functions for now)
def task_detail(request, task_id):
	task = Task.objects.get(id=task_id)
	context = {'task': task}
	return render(request, 'tasks/task_detail.html', context)

def create_task(request):
	# Placeholder for task creation logic
	return render(request, 'tasks/create_task.html')

def update_task(request, task_id):
	# Placeholder for task update logic
	task = Task.objects.get(id=task_id)
	context = {'task': task}
	return render(request, 'tasks/update_task.html', context)

def delete_task(request, task_id):
	# Placeholder for task deletion logic
	task = Task.objects.get(id=task_id)
	context = {'task': task}
	return render(request, 'tasks/delete_task.html', context)

def toggle_complete(request, task_id):
	# Placeholder for task completion toggle logic
	task = Task.objects.get(id=task_id)
	context = {'task': task}
	return render(request, 'tasks/toggle_complete.html', context)

