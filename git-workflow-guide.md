# Git Workflow & Gestão de Branches para Django

Este guia vai ajudar você a entender o fluxo de trabalho profissional com Git para desenvolvimento e integração de features no projeto Django Task Manager.

## Estratégia de Branches

Uma estratégia eficiente de branches permite desenvolvimento paralelo, isolamento de features e integração controlada. Vamos adotar a seguinte estrutura:

```
master (ou main) - Branch de produção, sempre estável
     ↑
    dev - Branch de integração/desenvolvimento
  ↗   ↖   ↘
dev-feature1  dev-feature2  dev-feature3
```

### Nomenclatura de Branches

- **master/main**: Código de produção estável
- **dev**: Integração de features, pré-produção
- **dev-feature-name**: Feature específica em desenvolvimento (ex: dev-bucket-test, dev-auth)

## Explicação do Conflito de Migração

### O Problema

O Pull Request do aluno continha um problema comum com migrações Django. O arquivo `0003_include_bucket_schema.py` tinha dois erros principais:

1. **Dependências vazias**: A linha `dependencies = []` não estabelecia conexão com migrações anteriores
2. **Recriação de modelo existente**: A migração tentava criar novamente o modelo Task que já existia, em vez de apenas modificá-lo

O erro `table "tasks_task" already exists` ocorreu porque a migração tentou criar uma tabela que já existia no banco de dados.

### O que o aluno deveria ter feito

Para implementar corretamente o recurso de buckets, o aluno deveria:

1. **Configurar dependências corretas**:
   ```python
   dependencies = [
       ('tasks', '0002_alter_task_options_and_more'),
   ]
   ```

2. **Criar apenas o novo modelo e modificar o existente**:
   Em vez de recriar o modelo Task inteiro, o aluno deveria ter usado operações específicas para:
   - Criar o modelo Bucket (usando `CreateModel`)
   - Adicionar o campo bucket ao modelo Task existente (usando `AddField`)

3. **Usar ferramentas do Django**: Uma abordagem melhor seria deixar o Django gerar as migrações automaticamente:
   ```bash
   # Após adicionar o modelo Bucket e o campo bucket no models.py
   python manage.py makemigrations
   ```

### Como evitar esses problemas

Para evitar problemas semelhantes, ensine seus alunos a:

1. Sempre deixar o Django gerar migrações automaticamente quando possível
2. Nunca editar manualmente os arquivos de migração, a menos que seja absolutamente necessário
3. Se precisar editar migrações, entender o sistema de dependências do Django
4. Testar alterações em um ambiente de desenvolvimento antes de submeter um PR

## 1. Workflow para Testar Pull Requests

### Criando um Branch de Desenvolvimento

Quando um aluno submete um PR, siga esses passos para testá-lo de forma segura:

```bash
# Verifique em qual branch você está
git status

# Crie uma nova branch de desenvolvimento para teste
git checkout -b dev-feature-test

# Puxe as alterações do PR para sua branch de teste (substitua 1 pelo número do PR)
git pull origin pull/1/head
```

### Testando as Alterações

Após baixar as alterações, verifique se tudo funciona:

```bash
# Aplicar migrações
python manage.py migrate

# Iniciar o servidor
python manage.py runserver
```

Teste todas as funcionalidades manualmente no navegador.

## 2. Resolvendo Conflitos de Migração

Quando ocorrer o erro `table "tasks_task" already exists` ou `Conflicting migrations detected`, siga estes passos:

## 2. Resolvendo Conflitos de Migração

Quando ocorrer o erro `table "tasks_task" already exists` ou `Conflicting migrations detected`, siga estes passos:

### 2.1. Identificar o Problema

Primeiro, verifique os arquivos de migração para entender o conflito:

```bash
# Liste as migrações existentes
ls tasks/migrations/
```

### 2.2. Criar uma Nova Migração Corrigida

```bash
# Faça backup da migração problemática
mv tasks/migrations/0003_include_bucket_schema.py tasks/migrations/0003_include_bucket_schema.py.bak

# Crie uma nova migração vazia
python manage.py makemigrations tasks --empty --name create_bucket_model
```

### 2.3. Editar a Nova Migração

Edite o arquivo de migração criado (normalmente `0003_create_bucket_model.py`) e substitua seu conteúdo pelo código correto que adiciona apenas os novos campos/modelos.

### 2.4. Aplicar a Migração Corrigida

```bash
python manage.py migrate
```

## 3. Fluxo de Trabalho com Git & GitHub

Aqui está o fluxo de trabalho completo para desenvolvimento com branches no Git:

### 3.1. Configuração Inicial

```bash
# Clone o repositório
git clone git@github.com:username/django-task-manager.git
cd django-task-manager

# Crie e mude para um branch de desenvolvimento
git checkout -b dev
git push -u origin dev  # Crie o branch no GitHub também
```

### 3.2. Desenvolvimento de Features

Para cada nova feature, crie um branch dedicado a partir do dev:

```bash
# Criar branch para uma nova feature
git checkout dev
git checkout -b dev-feature-name

# Trabalhe e faça commits frequentes
git add .
git commit -m "Mensagem descritiva sobre a mudança"

# Sincronize com o GitHub regularmente
git push -u origin dev-feature-name
```

### 3.3. Revisão de Pull Request (PR)

Quando a feature estiver pronta:

1. Vá para o GitHub e crie um Pull Request do seu branch `dev-feature-name` para o branch `dev`
2. Peça a um colega para revisar seu código
3. Faça os ajustes necessários baseados no feedback

### 3.4. Testando um Pull Request Localmente

Se você receber um PR para revisar, siga estes passos:

```bash
# Crie um branch de teste local para o PR
git checkout dev
git checkout -b test-feature-name

# Puxe as alterações do PR
git pull origin pull/1/head   # Substitua 1 pelo número do PR

# Teste a feature
python manage.py migrate
python manage.py runserver
```

### 3.5. Exemplo Prático: Correção do Bucket Feature

Vamos ver um exemplo real de como lidar com a correção do feature de buckets:

```bash
# Estando no branch dev-bucket-test com as alterações do PR
git status  # Verificar arquivos modificados

# Commit das correções de migração
git add tasks/migrations/0003_create_bucket_model.py
git rm tasks/migrations/0003_include_bucket_schema.py
git commit -m "Fix: Corrigido problema de migração do bucket"

# Sincronizar com o GitHub
git push -u origin dev-bucket-test  # Se o branch ainda não existir no remoto
# OU
git push  # Se o branch já existir no remoto
```

### 3.6. Integrando a Feature no Branch de Desenvolvimento

Após testar e verificar que a feature está funcionando corretamente:

```bash
# Voltar para o branch de desenvolvimento
git checkout dev

# Integrar a feature corrigida
git merge dev-bucket-test

# Resolver conflitos se necessário
# [edite os arquivos em conflito]
# git add .
# git commit

# Enviar para o GitHub
git push origin dev
```

### 3.7. Integrando Múltiplas Features

Quando tiver várias features prontas (por exemplo, buckets e autenticação):

```bash
# Já estando no branch dev com a primeira feature (buckets) integrada
# Integrar a segunda feature (autenticação)
git merge dev-auth

# Resolver conflitos se necessário
# Testar a aplicação completa

# Enviar para o GitHub
git push origin dev
```

### 3.8. Promoção para Produção (Master/Main)

Quando todas as features estiverem estáveis no branch dev:

```bash
# Mudar para o branch principal
git checkout master  # ou main

# Integrar as mudanças do branch de desenvolvimento
git merge dev

# Enviar para o GitHub
git push origin master
```

## 4. Boas Práticas para seu Projeto

1. **Commits Atômicos**: Faça commits pequenos e específicos, com mensagens descritivas
   ```bash
   git commit -m "Add: Implementação do modelo Bucket para categorizar tarefas"
   ```

2. **Prefixos para Commits**:
   - `Add:` Nova funcionalidade
   - `Fix:` Correção de bug
   - `Refactor:` Melhorias de código sem alterar comportamento
   - `Docs:` Alterações em documentação
   - `Style:` Formatação, não afeta o código
   - `Test:` Adição ou correção de testes

3. **Pull Requests Detalhados**: Inclua descrições completas:
   - O que a mudança faz
   - Por que ela é necessária
   - Como testá-la
   - Screenshots (se aplicável)

4. **Code Reviews**: Sempre faça revisão de código antes de mesclar

5. **Mantenha Branches Atualizados**:
   ```bash
   git checkout dev-feature-name
   git pull origin dev  # Obtenha as mudanças mais recentes do branch de desenvolvimento
   git rebase dev       # Reaplique seus commits sobre as mudanças do dev
   ```

## 5. Quando usar o Fluxo Completo

Este fluxo de trabalho é ideal para:

Explique para os alunos os seguintes pontos importantes:

### 7.1. Sobre Branches Git

1. **Isolamento de Trabalho**: Cada feature deve ser desenvolvida em seu próprio branch
2. **Experimentação Segura**: Branches permitem experimentar sem afetar o código estável
3. **Revisão de Código**: Pull Requests facilitam revisão antes da integração
4. **Histórico Organizado**: Mantém o histórico de desenvolvimento claro e compreensível

### 7.2. Sobre Migrações Django

1. **Nunca recrie modelos existentes**: Use `AlterField` ou `AddField` para modificar modelos existentes
2. **Dependências corretas**: Sempre garanta que as migrações dependem da migração anterior correta
3. **Teste as migrações**: Sempre teste migrações em ambiente de desenvolvimento primeiro
4. **Use `--empty` quando necessário**: Para situações complexas, migrações manuais são mais controláveis
5. **Deixe o Django gerar migrações automaticamente**: Em vez de criar manualmente, use `python manage.py makemigrations`

### 7.3. Corrigindo migrações como aluno

Se você é o aluno que enviou o PR com problemas de migração, aqui está como corrigir:

```bash
# 1. Volte seu branch para antes da migração problemática
git checkout feature/task_bucket
git reset --hard HEAD~1  # Volta um commit atrás (cuidado!)

# 2. Ajuste seus modelos corretamente em models.py
# (Adicione o modelo Bucket e o campo bucket ao Task)

# 3. Deixe o Django gerar a migração correta
python manage.py makemigrations

# 4. Verifique se a migração gerada está correta
cat tasks/migrations/0003_*.py

# 5. Teste a migração
python manage.py migrate

# 6. Faça commit e push das alterações
git add .
git commit -m "Fix: Correção da migração para o modelo Bucket"
git push origin feature/task_bucket --force  # Cuidado com --force!
```

> **Observação**: O uso de `git reset --hard` e `git push --force` são perigosos e devem ser usados com cautela, pois reescrevem o histórico. Em projetos de equipe, coordene com os colegas antes de usar.

## 8. GitHub CLI (Alternativa mais Simples)

Se você tem o GitHub CLI instalado, pode testar PRs mais facilmente:

```bash
# Autenticar no GitHub (apenas na primeira vez)
gh auth login

# Verificar PRs abertos
gh pr list

# Fazer checkout do PR para teste
gh pr checkout 1  # Substitua 1 pelo número do PR

# Após testar, mesclar diretamente
gh pr merge 1  # Várias opções de merge serão oferecidas
```

---

## Recursos Adicionais

- [Documentação de Migrações do Django](https://docs.djangoproject.com/en/5.2/topics/migrations/)
- [Workflow do Git com PRs](https://guides.github.com/introduction/flow/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
