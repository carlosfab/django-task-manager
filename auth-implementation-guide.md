# Implementação de Autenticação no Django Task Manager

Este guia apresenta o plano completo para implementar autenticação no projeto Django Task Manager, partindo do branch `dev-auth` até sua integração final no branch `dev`.

## 1. Visão Geral da Feature

A implementação de autenticação vai permitir:
- Registro de usuários
- Login/Logout
- Tarefas associadas a usuários específicos
- Proteção de páginas (visíveis apenas para usuários autenticados)
- Gerenciamento básico de perfil de usuário

## 2. Planejamento da Autenticação

### 2.1. Componentes a Serem Desenvolvidos

1. **Modelos**:
   - Atualizar o modelo `Task` para incluir referência ao `User`
   - Opcionalmente: Atualizar o modelo `Bucket` para estar associado a usuários

2. **Páginas de Autenticação**:
   - Login (`accounts/login.html`)
   - Registro (`accounts/register.html`)
   - Redefinição de Senha (`accounts/password_reset.html`)
   - Perfil do Usuário (`accounts/profile.html`)

3. **Navegação**:
   - Atualizar `base.html` para mostrar estado de login e opções relevantes

4. **Proteção de Views**:
   - Aplicar `login_required` às views existentes
   - Filtrar tarefas por usuário atual

### 2.2. Estrutura de Arquivos

```
taskmanager/
├── accounts/                    # Nova aplicação 
│   ├── templates/accounts/
│   │   ├── login.html            
│   │   ├── register.html        
│   │   ├── profile.html         
│   │   └── password_reset.html  
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                 # Formulários personalizados
│   ├── models.py                # Perfil de usuário (se necessário)
│   ├── urls.py                  # Rotas de autenticação
│   └── views.py                 # Views de autenticação
├── tasks/
│   ├── models.py                # Atualizar com campo user
│   ├── views.py                 # Atualizar para usar @login_required
│   └── ...                      # Outros arquivos existentes
└── ...                          # Outros arquivos do projeto
```

## 3. Implementação Passo-a-Passo

### Passo 1: Criar Aplicativo de Contas

```bash
# Criar aplicativo
python manage.py startapp accounts

# Criar estrutura de diretórios
mkdir -p accounts/templates/accounts
```

### Passo 2: Configurar Settings

Edite `taskmanager/settings.py`:

```python
INSTALLED_APPS = [
    # ... apps existentes
    'accounts',
]

# Configurações de login
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/tarefas/'
LOGOUT_REDIRECT_URL = '/'
```

### Passo 3: Atualizar o Modelo Task

Edite `tasks/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Bucket(models.Model):
    # ... código existente
    # Opcionalmente, adicionar:
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buckets', null=True, blank=True)

class Task(models.Model):
    # ... campos existentes
    
    # Adicionar relação com usuário
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name='Usuário',
        null=True,  # Temporário, para migração
    )
    
    # ... resto do código existente
```

### Passo 4: Criar Migração e Migrar

```bash
# Criar migração
python manage.py makemigrations

# Aplicar migração
python manage.py migrate
```

### Passo 5: Criar URLs de Autenticação

Crie `accounts/urls.py`:

```python
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', include('django.contrib.auth.urls')),  # Inclui login, logout, reset de senha
]
```

Atualize `taskmanager/urls.py`:

```python
urlpatterns = [
    # ... URLs existentes
    path('accounts/', include('accounts.urls')),
]
```

### Passo 6: Criar Views de Autenticação

Edite `accounts/views.py`:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
            return redirect('tasks:task_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
```

### Passo 7: Criar Formulário de Registro Melhorado (Opcional)

Crie `accounts/forms.py`:

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

Atualize `accounts/views.py` para usar o formulário melhorado:

```python
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # ... resto do código
    else:
        form = UserRegisterForm()
    # ... resto do código
```

### Passo 8: Criar Templates de Autenticação

Crie `accounts/templates/accounts/register.html`:

```html
{% extends 'tasks/base.html' %}

{% block content %}
<div class="row fade-in py-4">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-header">
                <h2><i class="fas fa-user-plus me-2"></i>Registrar Nova Conta</h2>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    {% for field in form %}
                    <div class="mb-3">
                        <label for="{{ field.id_for_label }}" class="form-label">
                            {{ field.label }}
                        </label>
                        {{ field }}
                        {% if field.errors %}
                        <div class="text-danger">
                            {{ field.errors }}
                        </div>
                        {% endif %}
                        {% if field.help_text %}
                        <small class="form-text text-muted">{{ field.help_text }}</small>
                        {% endif %}
                    </div>
                    {% endfor %}
                    
                    <button type="submit" class="btn btn-primary btn-icon">
                        <i class="fas fa-user-plus me-2"></i>Registrar
                    </button>
                </form>
                <div class="mt-3">
                    <p>Já tem uma conta? <a href="{% url 'accounts:login' %}">Faça Login</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Crie `accounts/templates/accounts/login.html`:

```html
{% extends 'tasks/base.html' %}

{% block content %}
<div class="row fade-in py-4">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-header">
                <h2><i class="fas fa-sign-in-alt me-2"></i>Login</h2>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label">
                            <i class="fas fa-user me-2 text-muted"></i>Usuário
                        </label>
                        {{ form.username }}
                    </div>
                    
                    <div class="mb-3">
                        <label for="{{ form.password.id_for_label }}" class="form-label">
                            <i class="fas fa-lock me-2 text-muted"></i>Senha
                        </label>
                        {{ form.password }}
                    </div>
                    
                    <button type="submit" class="btn btn-primary btn-icon">
                        <i class="fas fa-sign-in-alt me-2"></i>Entrar
                    </button>
                </form>
                <div class="mt-3">
                    <p>Não tem uma conta? <a href="{% url 'accounts:register' %}">Registre-se</a></p>
                    <p><a href="{% url 'accounts:password_reset' %}">Esqueci minha senha</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Crie `accounts/templates/accounts/profile.html`:

```html
{% extends 'tasks/base.html' %}

{% block content %}
<div class="row fade-in py-4">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-header">
                <h2><i class="fas fa-user-circle me-2"></i>Perfil do Usuário</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4 text-center mb-4">
                        <i class="fas fa-user-circle fa-6x text-primary mb-3"></i>
                        <h3>{{ user.username }}</h3>
                        <p class="text-muted">{{ user.email }}</p>
                    </div>
                    <div class="col-md-8">
                        <h4><i class="fas fa-info-circle me-2"></i>Informações da Conta</h4>
                        <ul class="list-group mt-3">
                            <li class="list-group-item">
                                <i class="fas fa-user me-2 text-muted"></i>
                                <strong>Nome de Usuário:</strong> {{ user.username }}
                            </li>
                            <li class="list-group-item">
                                <i class="fas fa-envelope me-2 text-muted"></i>
                                <strong>Email:</strong> {{ user.email|default:"Não informado" }}
                            </li>
                            <li class="list-group-item">
                                <i class="fas fa-calendar-alt me-2 text-muted"></i>
                                <strong>Membro desde:</strong> {{ user.date_joined|date:"d/m/Y" }}
                            </li>
                        </ul>

                        <h4 class="mt-4"><i class="fas fa-chart-bar me-2"></i>Estatísticas</h4>
                        <ul class="list-group mt-3">
                            <li class="list-group-item">
                                <i class="fas fa-tasks me-2 text-muted"></i>
                                <strong>Total de Tarefas:</strong> {{ user.tasks.count }}
                            </li>
                            <li class="list-group-item">
                                <i class="fas fa-check me-2 text-muted"></i>
                                <strong>Tarefas Concluídas:</strong> {{ user.tasks.filter.completed.count }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="card-footer text-center">
                <a href="{% url 'accounts:password_change' %}" class="btn btn-primary btn-icon">
                    <i class="fas fa-key me-2"></i>Alterar Senha
                </a>
                <a href="{% url 'tasks:task_list' %}" class="btn btn-secondary btn-icon ms-2">
                    <i class="fas fa-tasks me-2"></i>Minhas Tarefas
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Passo 9: Atualizar o Template Base para Exibir Estado de Login

Edite `tasks/templates/tasks/base.html` (barra de navegação):

```html
<div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav ms-auto">
        <li class="nav-item">
            <a class="nav-link" href="{% url 'tasks:home' %}">
                <i class="fas fa-home me-1"></i> Início
            </a>
        </li>
        
        {% if user.is_authenticated %}
            <li class="nav-item">
                <a class="nav-link" href="{% url 'tasks:task_list' %}">
                    <i class="fas fa-tasks me-1"></i> Tarefas
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{% url 'tasks:create_task' %}">
                    <i class="fas fa-plus-circle me-1"></i> Nova Tarefa
                </a>
            </li>
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                    <i class="fas fa-user me-1"></i> {{ user.username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="{% url 'accounts:profile' %}">
                        <i class="fas fa-id-card me-2"></i>Perfil
                    </a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="{% url 'accounts:logout' %}">
                        <i class="fas fa-sign-out-alt me-2"></i>Sair
                    </a></li>
                </ul>
            </li>
        {% else %}
            <li class="nav-item">
                <a class="nav-link" href="{% url 'accounts:login' %}">
                    <i class="fas fa-sign-in-alt me-1"></i> Login
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{% url 'accounts:register' %}">
                    <i class="fas fa-user-plus me-1"></i> Registrar
                </a>
            </li>
        {% endif %}
    </ul>
</div>
```

### Passo 10: Proteger as Views e Filtrar por Usuário

Atualize `tasks/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task, Bucket
from .forms import TaskForm

# Adicione @login_required a todas as views relevantes
@login_required
def task_list(request):
    # Filtrar tarefas por usuário atual
    tasks = Task.objects.filter(user=request.user).order_by('bucket__order', 'bucket__name', '-priority', 'due_date')
    buckets = Bucket.objects.all()  # Ou filtre por usuário se buckets for específico por usuário
    
    # Resto do código igual...
    
@login_required
def task_detail(request, task_id):
    # Garantir que o usuário só acesse suas próprias tarefas
    task = get_object_or_404(Task, id=task_id, user=request.user)
    # Resto do código igual...

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associar ao usuário atual
            task.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('tasks:task_list')
    # Resto do código igual...

# Continue com as outras views...
```

### Passo 11: Criar Dados Iniciais para Usuários Existentes

Crie uma migração para associar tarefas existentes a um usuário padrão:

```bash
python manage.py makemigrations tasks --empty --name associate_tasks_to_users
```

Edite a migração criada:

```python
# tasks/migrations/XXXX_associate_tasks_to_users.py

def associate_tasks(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    User = apps.get_model('auth', 'User')
    
    # Pegar primeiro superusuário ou criar um se não existir
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if admin_user:
        # Associar todas as tarefas sem usuário ao admin
        Task.objects.filter(user__isnull=True).update(user=admin_user)

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', 'XXXX_previous_migration'),  # Substitua pelo nome da migração anterior
    ]

    operations = [
        migrations.RunPython(associate_tasks),
    ]
```

### Passo 12: Testar e Ajustar

1. **Aplicar Migrações**:
   ```bash
   python manage.py migrate
   ```

2. **Criar Superusuário** (se ainda não tiver):
   ```bash
   python manage.py createsuperuser
   ```

3. **Criar Usuários de Teste**:
   - Crie alguns usuários normais usando a página de registro

4. **Testar Funcionalidades**:
   - Login/logout
   - Criação de tarefas (verificar se são associadas ao usuário correto)
   - Visibilidade de tarefas (verificar se usuários só veem suas próprias tarefas)
   - Restrições de acesso (verificar se páginas são protegidas)

### Passo 13: Finalizar e Integrar

```bash
# Commit das alterações
git add .
git commit -m "Add: Implementação completa do sistema de autenticação de usuários"

# Enviar para o repositório remoto
git push origin dev-auth

# Voltar para o branch de desenvolvimento
git checkout dev

# Mesclar as alterações
git merge dev-auth

# Resolver conflitos, se houver
# [Se necessário] git add . && git commit -m "Merge: Integração da feature de autenticação"

# Enviar para o repositório remoto
git push origin dev
```

## 4. Observações Importantes

1. **Criação de Usuários**:
   - Crie pelo menos um usuário superusuário: `python manage.py createsuperuser`
   - Crie 2-3 usuários regulares para testes
   - Distribua algumas tarefas entre os usuários

2. **Buckets Compartilhados ou Por Usuário**:
   - A implementação atual mantém os buckets compartilhados entre todos os usuários
   - Se desejar buckets por usuário, adicione campo `user` ao modelo `Bucket` e atualize views

3. **Limpeza Pós-Migração**:
   - Após testar e confirmar que tudo funciona, você pode remover o `null=True` do campo `user` no modelo `Task`
   - Faça uma nova migração para tornar o campo obrigatório

4. **Segurança Adicional**:
   - Todas as views importantes estão protegidas com `@login_required`
   - As consultas filtram por `user=request.user` para garantir que usuários só vejam suas próprias tarefas

## 5. Próximos Passos (Futuras Melhorias)

1. **Confirmação de Email** - Implementar verificação por email
2. **Recuperação de Senha** - Adicionar templates personalizados para reset de senha
3. **Perfil Expandido** - Adicionar foto de perfil, detalhes adicionais
4. **Compartilhamento de Tarefas** - Permitir compartilhar tarefas entre usuários
5. **Estatísticas de Usuário** - Dashboard com gráficos de progresso

---

Este guia fornece um roadmap completo para implementar autenticação no Task Manager. Ao seguir esses passos, você criará um sistema que permite múltiplos usuários e protege os dados de cada usuário, seguindo as melhores práticas de segurança e design do Django.
