# NomNom API - Backend

API FastAPI integrada com Supabase para o projeto NomNom.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Supabase** - Backend as a Service (base de dados)
- **Uvicorn** - Servidor ASGI de alta performance
- **Pydantic** - Validação de dados

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase com projeto criado

## ⚙️ Configuração

### 1. Instalar dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Supabase:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

Para obter essas credenciais:
1. Acesse seu projeto no [Supabase](https://supabase.com)
2. Vá em Settings > API
3. Copie a `URL` e a `anon/public key`

### 3. Executar o servidor

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗂️ Estrutura do Projeto

```
backend/
├── main.py              # Aplicação principal FastAPI
├── config.py            # Configurações e variáveis de ambiente
├── database.py          # Cliente Supabase
├── models.py            # Modelos Pydantic (validação)
├── routers/             # Rotas da API
│   ├── __init__.py
│   └── example.py       # Exemplo de CRUD
├── requirements.txt     # Dependências Python
├── .env.example         # Template de variáveis de ambiente
└── .gitignore          # Arquivos ignorados pelo Git
```

## 🔌 Usando a API

### Exemplo: Criar uma tabela no Supabase

No Supabase SQL Editor, crie uma tabela exemplo:

```sql
CREATE TABLE items (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar acesso público (ajuste conforme necessário)
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON items
  FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON items
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON items
  FOR UPDATE USING (true);

CREATE POLICY "Enable delete access for all users" ON items
  FOR DELETE USING (true);
```

### Endpoints disponíveis

- `GET /` - Informações da API
- `GET /health` - Health check
- `GET /api/v1/items` - Listar todos os itens
- `GET /api/v1/items/{id}` - Obter item específico
- `POST /api/v1/items` - Criar novo item
- `PUT /api/v1/items/{id}` - Atualizar item
- `DELETE /api/v1/items/{id}` - Deletar item

## 🔧 Personalização

### Adicionar novos endpoints

1. Crie um novo arquivo em `routers/`, por exemplo `users.py`
2. Defina os modelos em `models.py`
3. Crie as rotas usando o padrão do `example.py`
4. Importe e registre o router em `main.py`:

```python
from routers import users

app.include_router(users.router, prefix="/api/v1", tags=["users"])
```

## 🔒 Segurança

- Configure as políticas de RLS (Row Level Security) no Supabase
- Em produção, especifique os domínios permitidos no CORS
- Use variáveis de ambiente para dados sensíveis
- Nunca commite o arquivo `.env`

## 📝 Notas

- O arquivo `example.py` é apenas um modelo - ajuste conforme suas necessidades
- Personalize os modelos em `models.py` de acordo com seu banco de dados
- Para autenticação, considere usar o Supabase Auth

## 🤝 Contribuindo

Este é um template inicial. Adapte conforme as necessidades do seu projeto!
