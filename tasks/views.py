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