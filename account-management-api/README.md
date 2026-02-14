# Account Management API

API de gerenciamento de contas usando **FastAPI** e **Supabase**.

## 🚀 Funcionalidades

- ✅ Criação de contas com validação
- ✅ Visualização de contas (individual e lista)
- ✅ Atualização de dados da conta
- ✅ Exclusão de contas
- ✅ Autenticação com Supabase Auth (login/logout)
- ✅ Suporte a JWT tokens
- ✅ Documentação automática (Swagger/OpenAPI)

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase (gratuita)
- pip ou poetry

## 🔧 Instalação

1. Clone o repositório:
```bash
cd account-management-api
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Supabase:
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

## 🗄️ Configuração do Supabase

### 1. Criar projeto no Supabase
- Acesse [supabase.com](https://supabase.com)
- Crie um novo projeto
- Copie a URL e a chave anon do projeto

### 2. Criar tabela `profiles` (opcional)
Se quiser armazenar dados adicionais além do Supabase Auth, crie uma tabela:

```sql
create table profiles (
  id uuid references auth.users on delete cascade primary key,
  email text unique not null,
  name text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now())
);

-- Habilitar RLS (Row Level Security)
alter table profiles enable row level security;

-- Criar policies
create policy "Users can view their own profile" 
  on profiles for select 
  using (auth.uid() = id);

create policy "Users can update their own profile" 
  on profiles for update 
  using (auth.uid() = id);
```

### 3. Habilitar Email Auth
- No painel do Supabase, vá em Authentication > Providers
- Habilite "Email"

## ▶️ Executando

```bash
uvicorn src.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

Acesse a documentação interativa:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### Accounts

#### `POST /accounts/`
Cria uma nova conta
```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

#### `GET /accounts/{account_id}`
Busca uma conta por ID (UUID)

#### `GET /accounts/`
Lista todas as contas (com paginação)
- Query params: `limit` (1-1000, default: 100), `offset` (default: 0)

#### `PUT /accounts/{account_id}`
Atualiza dados de uma conta
```json
{
  "name": "João da Silva",
  "email": "joao.silva@example.com"
}
```

#### `DELETE /accounts/{account_id}`
Deleta uma conta

### Authentication

#### `POST /auth/login`
Realiza login
```json
{
  "email": "joao@example.com",
  "password": "senha123"
}
```

Resposta:
```json
{
  "user": {
    "id": "uuid",
    "email": "joao@example.com",
    "name": "João Silva",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "access_token": "eyJ...",
  "refresh_token": "refresh_token",
  "expires_in": 3600,
  "token_type": "bearer",
  "message": "Login realizado com sucesso"
}
```

#### `POST /auth/logout`
Realiza logout

#### `GET /auth/me`
Retorna dados do usuário autenticado
- Header: `Authorization: Bearer {access_token}`

## 📦 Estrutura do Projeto

```
account-management-api/
├── src/
│   ├── main.py              # Aplicação FastAPI
│   ├── config.py            # Configurações
│   ├── database.py          # Cliente Supabase
│   ├── models/              # Modelos de dados
│   │   ├── __init__.py
│   │   └── account.py
│   ├── routers/             # Rotas da API
│   │   ├── __init__.py
│   │   ├── accounts.py      # CRUD de contas
│   │   └── auth.py          # Autenticação
│   ├── schemas/             # Schemas Pydantic
│   │   ├── __init__.py
│   │   └── account.py
│   ├── services/            # Lógica de negócio
│   │   ├── __init__.py
│   │   └── account_service.py
│   └── utils/               # Utilitários
│       ├── __init__.py
│       └── validators.py
├── .env                     # Variáveis de ambiente
├── .env.example             # Exemplo de .env
├── requirements.txt         # Dependências
└── README.md
```

## 🔐 Segurança

- As senhas são gerenciadas pelo Supabase Auth (hashing automático)
- Use HTTPS em produção
- Nunca exponha suas chaves do Supabase no código
- Configure CORS adequadamente para produção
- Implemente rate limiting para produção

## 🧪 Testando

### Criar uma conta
```bash
curl -X POST "http://localhost:8000/accounts/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Teste User",
    "email": "teste@example.com",
    "password": "senha123"
  }'
```

### Fazer login
```bash
curl -X POST "http://localhost:8000/auth/login" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "teste@example.com",
    "password": "senha123"
  }'
```

### Buscar conta
```bash
curl -X GET "http://localhost:8000/accounts/{account_id}"
```

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Supabase**: Backend as a Service (Auth + Database)
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **Python 3.8+**: Linguagem de programação

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.