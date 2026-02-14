# 🔐 Sistema de Autenticação - NomNom API

Sistema completo de criação de conta e autenticação usando Supabase Auth.

## Endpoints Disponíveis

### 1. Criar Conta (Sign Up)
```http
POST /api/v1/auth/signup
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senhaSegura123",
  "name": "Nome do Usuário"
}
```

**Resposta (201 Created):**
```json
{
  "id": "uuid-do-usuario",
  "email": "usuario@exemplo.com",
  "name": "Nome do Usuário",
  "created_at": "2026-02-14T10:30:00Z"
}
```

### 2. Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senhaSegura123"
}
```

**Resposta (200 OK):**
```json
{
  "user": {
    "id": "uuid-do-usuario",
    "email": "usuario@exemplo.com",
    "name": "Nome do Usuário",
    "created_at": "2026-02-14T10:30:00Z"
  },
  "session": {
    "access_token": "eyJhbGc...",
    "refresh_token": "v1.MR...",
    "expires_in": 3600,
    "token_type": "bearer"
  },
  "message": "Login realizado com sucesso"
}
```

### 3. Logout
```http
POST /api/v1/auth/logout
```

### 4. Obter Usuário Atual
```http
GET /api/v1/auth/me
Authorization: Bearer {access_token}
```

## 📝 Personalização

### Adicionar Campos Personalizados

Edite os arquivos conforme seus campos da base de dados:

#### 1. models.py
```python
class UserCreate(BaseModel):
    """Modelo para criação de conta"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    
    # ADICIONE SEUS CAMPOS AQUI:
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    birth_date: Optional[date] = None
    bio: Optional[str] = None
    # etc...
```

#### 2. routers/auth.py

**Na função `create_account`:**

```python
# Adicione campos no user_metadata
auth_response = supabase.auth.sign_up({
    "email": user_data.email,
    "password": user_data.password,
    "options": {
        "data": {
            "name": user_data.name,
            # ADICIONE AQUI:
            "phone": user_data.phone,
            "avatar_url": user_data.avatar_url,
        }
    }
})
```

**Se você tem uma tabela customizada (ex: `profiles`):**

```python
# Descomentar e personalizar:
profile_data = {
    "id": auth_response.user.id,
    "name": user_data.name,
    "email": user_data.email,
    "phone": user_data.phone,
    "bio": user_data.bio,
    # outros campos...
}
supabase.table("profiles").insert(profile_data).execute()
```

### Atualizar UserResponse

Se adicionou campos, atualize também o modelo de resposta:

```python
class UserResponse(BaseModel):
    """Modelo de resposta após criação/login (sem senha)"""
    id: str
    email: str
    name: str
    created_at: datetime
    
    # ADICIONE SEUS CAMPOS:
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
```

## 🗄️ Configuração da Base de Dados

### Opção 1: Usar apenas Supabase Auth (user_metadata)

O Supabase Auth já armazena os usuários. Campos extras podem ir no `user_metadata`.

### Opção 2: Tabela Customizada (Recomendado)

Crie uma tabela `profiles` no Supabase:

```sql
-- Criar tabela profiles
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS (Row Level Security)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Política: Usuários podem ler apenas o próprio perfil
CREATE POLICY "Users can read own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

-- Política: Usuários podem inserir o próprio perfil
CREATE POLICY "Users can insert own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Política: Usuários podem atualizar o próprio perfil
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

## 🔒 Segurança

### No Supabase Dashboard:

1. **Confirmar Email**: Em Authentication > Settings, configure:
   - Email confirmations (opcional)
   - Password requirements (recomendado: mínimo 6 caracteres)

2. **Rate Limiting**: Configure limites de requisições

3. **SMTP**: Configure envio de emails de confirmação

### No Código:

- Senhas nunca são retornadas nas respostas
- Use HTTPS em produção
- Armazene tokens de forma segura no frontend (não em localStorage se possível)

## 🧪 Testando

### No Swagger UI (http://localhost:8000/docs):

1. Expanda POST `/api/v1/auth/signup`
2. Clique em "Try it out"
3. Preencha os dados
4. Execute

### Com cURL:

```bash
# Criar conta
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123",
    "name": "Usuário Teste"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123"
  }'
```

## 🚀 Próximos Passos

1. ✅ Configure suas credenciais no `.env`
2. ✅ Personalize os campos em `models.py`
3. ✅ Crie tabela `profiles` no Supabase (se necessário)
4. ✅ Teste os endpoints
5. ⬜ Implemente middleware de autenticação
6. ⬜ Adicione refresh token
7. ⬜ Implemente recuperação de senha

## ⚠️ Notas Importantes

- O endpoint `/me` é um exemplo básico. Para produção, implemente um middleware que valida o token automaticamente
- Guarde o `access_token` retornado no login - ele será necessário para endpoints autenticados
- O token expira após o tempo definido em `expires_in` (geralmente 3600 segundos = 1 hora)
