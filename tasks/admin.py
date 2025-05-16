from django.contrib import admin
from .models import Task
from .models import Bucket

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'due_date', 'completed', 'created_at')
    list_filter = ('priority', 'completed', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('priority', 'completed')

class BucketAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)
    search_fields = ('name',)

admin.site.register(Bucket, BucketAdmin)
admin.site.register(Task, TaskAdmin)

