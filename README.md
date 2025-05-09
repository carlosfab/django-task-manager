<div align="center">
  <img src="https://sigmoidal.ai/wp-content/uploads/2025/05/Light-Blue-Academia-Sigmoidal-Logo-Isolado.png" alt="Logo Academia Sigmoidal" width="200">
  <h1>Gerenciador de Tarefas em Django</h1>
  <p>Um aplicativo web para gerenciamento de tarefas construído com Django</p>
  
  <p>
    <a href="#sobre">Sobre</a> •
    <a href="#demonstração">Demonstração</a> •
    <a href="#recursos">Recursos</a> •
    <a href="#instalação">Instalação</a> •
    <a href="#uso">Uso</a> •
    <a href="#tecnologias">Tecnologias</a> •
    <a href="#contribuição">Contribuição</a>
  </p>
</div>

## Sobre

Este projeto é um gerenciador de tarefas completo desenvolvido pelos alunos dos cursos de Pós-Graduação da [Academia Sigmoidal](http://sigmoidal.ai/cursos/). O aplicativo permite criar, visualizar, atualizar e excluir tarefas, organizadas em um layout Kanban com tarefas pendentes e concluídas.

Oferece recursos como gerenciamento de prioridades, datas de vencimento e interface de usuário moderna e responsiva.

## Demonstração

![Demonstração do Gerenciador de Tarefas](https://via.placeholder.com/800x400?text=Demonstração+do+Gerenciador+de+Tarefas)

## Recursos

✅ **Gerenciamento Completo de Tarefas (CRUD):**
- Criar tarefas com título, descrição, data de vencimento e prioridade
- Visualizar detalhes das tarefas
- Atualizar informações das tarefas
- Excluir tarefas indesejadas

✅ **Interface Moderna:**
- Design responsivo com Bootstrap 5
- Ícones intuitivos com Font Awesome
- Elementos visuais para prioridades (Alta, Média, Baixa)
- Layout Kanban para melhor organização

✅ **Recursos Adicionais:**
- Feedback visual com mensagens de sucesso/erro
- Navegação intuitiva entre páginas
- Confirmação antes de excluir tarefas
- Mudança rápida de status das tarefas (concluída/pendente)

## Instalação

### Pré-requisitos

- Python 3.11 ou superior
- Poetry (gerenciador de dependências)
- Git

### Clone o repositório

```bash
git clone https://github.com/carlosfab/django-task-manager.git
cd django-task-manager
```

### Configure o ambiente virtual e instale as dependências com Poetry

Poetry é um gerenciador de dependências moderno para Python. Este projeto usa Poetry para gerenciar suas dependências.

1. Se você ainda não tem o Poetry instalado, instale seguindo as [instruções oficiais](https://python-poetry.org/docs/#installation)

2. Após clonar o repositório, instale as dependências:

```bash
poetry install
```

3. Ative o ambiente virtual:

```bash
poetry shell
```

### Configure o banco de dados

O projeto está configurado para usar SQLite por padrão. Execute as migrações para configurar o banco de dados:

```bash
python manage.py migrate
```

### Crie um superusuário (opcional)

Se quiser acessar o painel de administração do Django:

```bash
python manage.py createsuperuser
```

## Uso

### Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse o aplicativo em seu navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Primeiros passos

1. Acesse a página inicial
2. Clique em "Nova Tarefa" para adicionar sua primeira tarefa
3. Preencha os detalhes da tarefa (título, descrição, prioridade, etc.)
4. Visualize suas tarefas pendentes e concluídas no layout Kanban
5. Gerencie suas tarefas conforme necessário

## Tecnologias

- **Backend:** Django 5.2
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Ícones:** Font Awesome 6
- **Banco de Dados:** SQLite (padrão)
- **Gerenciamento de Dependências:** Poetry
- **Formatação de Código:** Black, isort

## Estrutura do Projeto

A estrutura de arquivos principal do projeto é a seguinte:

```
django-task-manager/
├── manage.py              # Script para gerenciamento do Django
├── pyproject.toml         # Configuração do Poetry
├── poetry.lock            # Versões exatas das dependências
├── taskmanager/           # Projeto Django principal
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py            # Configuração de URLs principal
│   └── wsgi.py
└── tasks/                 # App de tarefas
    ├── __init__.py
    ├── admin.py           # Configuração do painel de administração
    ├── apps.py
    ├── forms.py           # Formulários para manipulação de tarefas
    ├── migrations/        # Migrações do banco de dados
    ├── models.py          # Modelos de dados
    ├── templates/         # Templates HTML
    │   └── tasks/
    │       ├── base.html
    │       ├── delete_task.html
    │       ├── home.html
    │       ├── task_detail.html
    │       ├── task_form.html
    │       └── task_list_kanban.html
    ├── tests.py           # Testes automatizados
    ├── urls.py            # URLs do app de tarefas
    └── views.py           # Lógica de visualização
```

## Contribuição

Este projeto foi desenvolvido como parte do curso de Pós-Graduação da [Academia Sigmoidal](http://sigmoidal.ai/cursos/). Se você é um aluno e deseja contribuir:

1. Faça um fork do repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Formate seu código com Black e isort (`black . && isort .`)
4. Faça commit das mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
5. Faça push para o branch (`git push origin feature/nova-funcionalidade`)
6. Abra um Pull Request

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

<div align="center">
  <p>Desenvolvido com ❤️ pelos alunos da <a href="http://sigmoidal.ai/cursos/">Academia Sigmoidal</a></p>
</div>