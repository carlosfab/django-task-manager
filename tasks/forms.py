# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se já tiver um valor, formatar no formato esperado pelo input date
        if self.instance.due_date:
            self.fields['due_date'].initial = self.instance.due_date.strftime('%Y-%m-%d')