from django.db import models

class Bucket(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    order = models.IntegerField(default=0, verbose_name='Ordem')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
    ]

    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de Vencimento')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name='Prioridade')
    completed = models.BooleanField(default=False, verbose_name='Concluída')

    bucket = models.ForeignKey(Bucket, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoria')

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-priority', 'due_date']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'