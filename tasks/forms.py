from django import forms
from .models import Task, Bucket

class TaskForm(forms.ModelForm):
    # Campo personalizado para permitir selecionar ou criar uma nova categoria
    bucket_choice = forms.ChoiceField(
        choices=[], 
        required=True, # Agora é obrigatório
        label="Categoria",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Campo para nova categoria caso o usuário queira criar uma
    new_bucket = forms.CharField(
        max_length=100, 
        required=False, 
        label="Nova Categoria",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da nova categoria'})
    )
    
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
        
        # Buscar todas as categorias e montar as opções
        bucket_choices = [('', 'Selecione uma categoria')]
        bucket_choices += [(str(bucket.id), bucket.name) for bucket in Bucket.objects.all().order_by('name')]
        bucket_choices.append(('new', '+ Criar nova categoria'))
        self.fields['bucket_choice'].choices = bucket_choices
        
        # Se a tarefa já tem uma categoria, selecionar como padrão
        if self.instance.pk and self.instance.bucket:
            self.fields['bucket_choice'].initial = str(self.instance.bucket.id)
    
    def clean(self):
        cleaned_data = super().clean()
        bucket_choice = cleaned_data.get('bucket_choice')
        new_bucket = cleaned_data.get('new_bucket')
        
        # Verificar se uma categoria foi selecionada
        if not bucket_choice:
            self.add_error('bucket_choice', 'Por favor, selecione uma categoria ou crie uma nova.')
            
        # Verificar se a opção de criar nova categoria foi selecionada mas nenhum nome foi fornecido
        elif bucket_choice == 'new' and not new_bucket:
            self.add_error('new_bucket', 'Por favor, informe um nome para a nova categoria.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        bucket_choice = self.cleaned_data.get('bucket_choice')
        new_bucket = self.cleaned_data.get('new_bucket')
        
        # Se selecionou criar nova categoria
        if bucket_choice == 'new' and new_bucket:
            # Cria ou busca uma categoria com esse nome
            bucket, created = Bucket.objects.get_or_create(name=new_bucket)
            instance.bucket = bucket
        # Se selecionou uma categoria existente
        elif bucket_choice and bucket_choice != 'new':
            instance.bucket = Bucket.objects.get(id=bucket_choice)
        # Este caso não deveria acontecer devido à validação, mas apenas por segurança
        else:
            instance.bucket = None
        
        if commit:
            instance.save()
        
        return instance