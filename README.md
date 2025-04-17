# Task Manager App - Component Summary

Before we start coding, let's understand the key components we'll be creating in our Django Task Manager application. This summary will give us a roadmap of what we're building.

## Project Structure

```
taskmanager/         # Main project folder
├── taskmanager/     # Project settings
│   ├── __init__.py
│   ├── settings.py  # Project configuration
│   ├── urls.py      # Main URL routing
│   ├── asgi.py      # ASGI config
│   └── wsgi.py      # WSGI config
├── tasks/           # Our tasks app
│   ├── __init__.py
│   ├── models.py    # Data models
│   ├── views.py     # View logic
│   ├── urls.py      # App-level URL routing
│   ├── forms.py     # Form definitions
│   ├── admin.py     # Admin configuration
│   └── templates/   # HTML templates
│       ├── base.html
│       └── tasks/   # Task-specific templates
│           ├── task_list.html
│           ├── task_detail.html
│           ├── task_form.html
│           └── task_confirm_delete.html
├── static/          # CSS, JS, images
└── manage.py        # Django management script
```

## Models (Data Structure)

We'll create one main model:

```python
# Task model - represents a single task
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.BooleanField(default=False)
```

## Views (Controllers)

We'll implement a full CRUD (Create, Read, Update, Delete) pattern using class-based views:

1. **TaskListView**: Shows all tasks (homepage)
2. **TaskDetailView**: Shows details of a specific task
3. **TaskCreateView**: Form for creating a new task
4. **TaskUpdateView**: Form for editing an existing task
5. **TaskDeleteView**: Confirmation for deleting a task
6. **task_toggle_complete**: Toggles the completion status of a task

## URLs (Routing)

We'll set up the following URL patterns:

1. `/tasks/` - List all tasks
2. `/tasks/create/` - Create a new task
3. `/tasks/<id>/` - View task details
4. `/tasks/<id>/update/` - Edit a task
5. `/tasks/<id>/delete/` - Delete a task
6. `/tasks/<id>/toggle/` - Toggle task completion

## Forms

We'll create a form for task creation and editing:

```python
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']
```

## Templates (Views)

We'll create HTML templates with Tailwind CSS styling:

1. **base.html** - Main layout template
2. **task_list.html** - List of all tasks
3. **task_detail.html** - Details of a specific task
4. **task_form.html** - Form for creating/editing tasks
5. **task_confirm_delete.html** - Confirmation page for deletion

## User Flow

1. User visits the homepage and sees a list of tasks
2. User can add a new task by clicking "Add Task"
3. User can view task details by clicking on a task title
4. User can edit or delete a task from the detail view
5. User can mark tasks as complete/incomplete from the list view

This structure follows Django's Model-View-Template pattern and implements best practices such as class-based views, proper URL namespacing, and form handling.