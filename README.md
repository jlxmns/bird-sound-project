# bird-sound-project
A web-based project that lets users see, create, update and delete birds from the database, upload audios and identify bird species by their cries and receive reports for most identified birds


## Requerimentos

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Gerenciador de pacotes e projetos

---

## Rodando o projeto

### 1. Instale o uv

Se você ainda não tem o uv instalado:

Usando curl:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Usando wget:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

Usando Powershell:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Usando pip ou pipx:
```bash
pipx install uv
```
```bash
pip install uv
```

Usando Homebrew:
```bash
brew install uv
```

### 2. Clone o repositório

```bash
git clone https://github.com/jlxmns/bird-sound-project.git
cd bird-sound-project
```

### 3. Instale as dependências

```bash
uv sync
```

Esse comando criará um virtual environment e instalará todas as dependências do `pyproject.toml` automaticamente.

### 4. Aplique as migrações no banco de dados

```bash
uv run python manage.py migrate
```

### 5. Rode o servidor de desenvolvimento

```bash
uv run python manage.py runbolt --dev
```

A API estará disponível em **http://127.0.0.1:8000**.

A documentação da API (OpenAPI) estará disponível em **http://127.0.0.1:8000/docs** ou **http://127.0.0.1:8000/docs/scalar**

O painel de administração estará disponível em **http://127.0.0.1:8000/admin**

---

## Passos opcionais

### Cria uma conta de administrador

Para acessar o painel de administração do django em `/admin`:

```bash
uv run python manage.py createsuperuser
```

Siga as instruções para definir um nome de usuário, email e senha.
