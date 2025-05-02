from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'due_date', 'completed', 'created_at')
    list_filter = ('priority', 'completed', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('priority', 'completed')

admin.site.register(Task, TaskAdmin)