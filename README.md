# OS System

Sistema de Ordem de Serviço desenvolvido com Flask e PostgreSQL.

Projeto criado com foco em desenvolvimento backend, arquitetura Flask, banco de dados relacional e boas práticas de desenvolvimento web.

## 🚀 Tecnologias Utilizadas

* Python
* Flask
* PostgreSQL
* SQLAlchemy
* Flask-Migrate
* HTML5
* CSS3
* Bootstrap 5
* JavaScript

---

## 📌 Funcionalidades Atuais

### Clientes

* Cadastro de clientes
* Edição de clientes
* Exclusão com modal Bootstrap
* Busca de clientes
* Paginação
* Ordenação
* Interface responsiva

### Ordens de Serviço

* Cadastro de ordens de serviço
* Relacionamento com clientes
* Status da ordem
* Listagem de ordens

---

## 🛠️ Estrutura do Projeto

```bash
app/
│
├── models/
├── routes/
├── templates/
├── static/
│
├── __init__.py
```

---

## ⚙️ Instalação

Clone o projeto:

```bash
git clone 
```

Crie ambiente virtual:

```bash
python -m venv venv
```

Ative ambiente virtual:

### Windows

```bash
venv\Scripts\activate
```

Instale dependências:

```bash
pip install -r requirements.txt
```

Configure arquivo `.env`:

```env
SECRET_KEY=sua_chave

DATABASE_URL=postgresql://postgres:SENHA@localhost:5432/os_system_db
```

Execute migrations:

```bash
flask db upgrade
```

Execute projeto:

```bash
flask run
```

---

## 📚 Objetivos do Projeto

Este projeto está sendo desenvolvido em etapas (V1, V2, V3), adicionando novas funcionalidades gradualmente, portfólio e utilização acadêmica.

---

## 🚧 Status do Projeto

Projeto em desenvolvimento.
