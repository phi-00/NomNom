# 🗄️ Setup Supabase - Passo a Passo

## 1️⃣ Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Clique em "New Project"
3. Preencha os dados:
   - **Project name**: Seu projeto (ex: "NomNom")
   - **Database password**: Escolha uma senha segura
   - **Region**: Escolha a região mais próxima
   - **Plan**: Clique em "Start with a free project"
4. Clique em "Create new project"

## 2️⃣ Obter Credenciais

1. Após criar o projeto, acesse o painel
2. Vá em **Settings** > **API** (ou acesse o Project Settings)
3. Copie:
   - **Project URL** (sua SUPABASE_URL)
   - **anon key** (sua SUPABASE_KEY)
4. Atualize o arquivo `.env`:
   ```env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua-chave-anon-aqui
   ```

## 3️⃣ Habilitar Email Auth

1. No painel do Supabase, vá em **Authentication**
2. Clique em **Providers**
3. Procure por "Email" e habilite
4. Configure as opções se necessário

## 4️⃣ Criar Tabela Profiles (Opcional)

Se quiser armazenar dados adicionais além do Supabase Auth:

1. No painel, vá em **SQL Editor**
2. Cole este código:

```sql
-- Criar tabela profiles
create table profiles (
  id uuid references auth.users on delete cascade primary key,
  email text unique not null,
  name text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now())
);

-- Adicionar comentário
comment on table profiles is 'Perfis de usuários';

-- Habilitar RLS (Row Level Security)
alter table profiles enable row level security;

-- Política: Usuários podem ver seu próprio perfil
create policy "Users can view their own profile"
  on profiles
  for select
  using (auth.uid() = id);

-- Política: Usuários podem atualizar seu próprio perfil
create policy "Users can update their own profile"
  on profiles
  for update
  using (auth.uid() = id);

-- Política: Usuários podem inserir seu próprio perfil
create policy "Users can insert their own profile"
  on profiles
  for insert
  with check (auth.uid() = id);
```

3. Clique em "Run" ou pressione Ctrl+Enter

## 5️⃣ Testar Conexão

1. Reinicie a API:
   ```bash
   python -m uvicorn src.main:app --reload
   ```

2. Acesse o Swagger: http://localhost:8000/docs

3. Tente criar uma conta:
   - Clique em "POST /accounts/"
   - Clique em "Try it out"
   - Preencha os dados:
     ```json
     {
       "name": "Seu Nome",
       "email": "seu_email@exemplo.com",
       "password": "senha_segura_123"
     }
     ```
   - Clique em "Execute"

## ✅ Verificação

Se tudo funcionar corretamente:
- ✓ Você verá a resposta com o ID da conta criada
- ✓ Os dados aparecerão na tabela `auth_users` do Supabase
- ✓ Se criou a tabela `profiles`, os dados aparecerão lá também

## 🐛 Troubleshooting

### Erro: "getaddrinfo failed"
- **Problema**: Conexão de rede ou DNS
- **Solução**: Verifique a internet, reinicie o router

### Erro: "Invalid API key"
- **Problema**: Chave Supabase inválida
- **Solução**: Copie novamente a chave do Supabase

### Erro: "Email already registered"
- **Problema**: Email já existe
- **Solução**: Use outro email para a conta de teste

### Erro: "Password should be at least 6 characters"
- **Problema**: Senha muito curta
- **Solução**: Use uma senha com no mínimo 6 caracteres

## 📚 Recursos Úteis

- [Documentação Supabase Auth](https://supabase.com/docs/guides/auth)
- [Documentação Supabase Database](https://supabase.com/docs/guides/database)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)

## 🎯 Próximos Passos

1. Experimente todos os endpoints no Swagger
2. Implemente meio de autenticação (middleware JWT)
3. Adicione rate limiting
4. Configure CORS para seu frontend
5. Deploy da aplicação
