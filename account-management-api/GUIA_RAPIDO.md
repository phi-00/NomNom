# 🚀 API Account Management - Guia Rápido

## Status da API
✅ **Servidor rodando**: http://localhost:8000

## 📚 Documentação Openness
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Principais

### ✅ Contas (Accounts)
- **POST** `/accounts/` - Criar nova conta
- **GET** `/accounts/{account_id}` - Buscar conta por ID
- **GET** `/accounts/` - Listar todas as contas (com paginação)
- **PUT** `/accounts/{account_id}` - Atualizar conta
- **DELETE** `/accounts/{account_id}` - Deletar conta

### 🔐 Autenticação (Auth)
- **POST** `/auth/login` - Login (retorna token JWT)
- **POST** `/auth/logout` - Logout
- **GET** `/auth/me` - Dados do usuário autenticado

## 📝 Exemplos de Uso

### 1. Criar uma conta
```bash
curl -X POST "http://localhost:8000/accounts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

### 3. Buscar conta
```bash
curl -X GET "http://localhost:8000/accounts/{account_id}"
```

### 4. Listar contas
```bash
curl -X GET "http://localhost:8000/accounts/?limit=10&offset=0"
```

### 5. Atualizar conta
```bash
curl -X PUT "http://localhost:8000/accounts/{account_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva Updated",
    "email": "joao.updated@example.com"
  }'
```

## 📋 Estrutura do Projeto
```
account-management-api/
├── src/
│   ├── main.py              # Aplicação FastAPI
│   ├── config.py            # Configurações
│   ├── database.py          # Cliente Supabase
│   ├── models/              # Modelos de dados
│   ├── routers/             # Rotas da API
│   │   ├── accounts.py      # CRUD de contas
│   │   └── auth.py          # Autenticação
│   ├── schemas/             # Schemas Pydantic
│   ├── services/            # Lógica de negócio
│   └── utils/               # Utilitários
├── .env                     # Variáveis de ambiente
├── requirements.txt         # Dependências
└── README.md               # Documentação
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## 🛠️ Tecnologias Utilizadas
- **FastAPI** - Framework web moderno
- **Supabase** - Backend as a Service (Auth + Database)
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **Python 3.8+** - Linguagem

## 💡 Próximas Ações Sugeridas

1. **Testar endpoints** na documentação interativa (http://localhost:8000/docs)
2. **Configurar banco de dados** - Criar tabela `profiles` no Supabase
3. **Implementar autenticação** - Adicionar middleware de verificação de tokens
4. **Adicionar validações** - Melhorar validators.py
5. **Deploy** - Publicar a API

## 📞 Suporte
- Verifique os logs do servidor para erros
- Consulte a documentação do FastAPI: https://fastapi.tiangolo.com
- Consulte a documentação do Supabase: https://supabase.com/docs
