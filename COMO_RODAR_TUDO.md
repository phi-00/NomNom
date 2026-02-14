# 🚀 Como Rodar Tudo - Backend + Frontend

## 📋 Pré-requisitos

- ✅ Node.js 18+ instalado
- ✅ Python 3.8+ instalado
- ✅ Conta Supabase configurada
- ✅ Backend já implementado

## 🎯 Passo 1: Instalar Dependências do Frontend

### Terminal 1

```bash
cd c:\Users\felip\OneDrive\Documentos\GitHub\NomNom\NomNom
npm install
```

Isso instalará:
- Vue 3.5.25
- Axios 1.6.2
- Vite 7.3.1
- E todas as dependências necessárias

**Tempo esperado**: 2-3 minutos

## 🎯 Passo 2: Iniciar Backend (Account Management API)

### Terminal 2

```bash
cd c:\Users\felip\OneDrive\Documentos\GitHub\NomNom\account-management-api
python -m uvicorn src.main:app --reload
```

**Saída esperada:**
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

**URL da API:**
- API: `http://localhost:8000`
- Documentação: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🎯 Passo 3: Iniciar Frontend (NomNom)

### Terminal 1 (após instalar dependências)

```bash
npm run dev
```

**Saída esperada:**
```
  VITE v7.3.1  ready in 123 ms

  ➜  Local:   http://localhost:5173/
```

**URL do Frontend:**
- Aplicação: `http://localhost:5173`

## ✅ Verificar se tudo está funcionando

### 1. Backend está respondendo?
```bash
curl http://localhost:8000/
# Resposta esperada: {"message": "Welcome to the Account Management API", ...}
```

### 2. Frontend está acessível?
```bash
curl http://localhost:5173/
# Resposta esperada: Arquivo HTML
```

### 3. Conexão funcionando?
1. Abra: `http://localhost:5173`
2. Clique em "Buscar Usuário"
3. Clique em "Carregar Usuários"
4. Se ver a lista, está tudo funcionando! ✅

## 🎬 Fluxo Completo de Teste

### 1. Criar uma Conta (Backend)

```bash
curl -X POST http://localhost:8000/accounts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

**Resposta esperada:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "João Silva",
  "email": "joao@example.com",
  "created_at": "2026-02-14T10:30:00Z"
}
```

### 2. Copie o ID retornado

### 3. Buscar no Frontend

1. Abra: `http://localhost:5173`
2. Clique em "Buscar Usuário"
3. Cole o ID no campo "Digite o ID do usuário"
4. Clique em "Buscar"
5. Veja os dados aparecer! ✅

### 4. Listar Usuários

1. Na mesma página
2. Clique em "Carregar Usuários"
3. A lista aparecerá na direita ✅

### 5. Editar Usuário

1. Com o usuário exibido, clique em "Editar"
2. Modifique o nome e/ou email
3. Clique em "Salvar Alterações"

### 6. Deletar Usuário

1. Com o usuário exibido, clique em "Deletar Usuário"
2. Confirme na caixa de diálogo
3. O usuário será removido ✅

## 🗂️ Estrutura de Pastas

```
C:\Users\felip\OneDrive\Documentos\GitHub\NomNom\
│
├── account-management-api/    (Backend - Python/FastAPI)
│   ├── src/
│   ├── .env
│   ├── requirements.txt
│   └── src/main.py (executar com uvicorn)
│
├── NomNom/                     (Frontend - Vue 3)
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── package-lock.json (após npm install)
│
└── backend/                    (Legado)
```

## 🔄 Workflow de Desenvolvimento

**Terminal 1 - Frontend**
```bash
cd NomNom
npm run dev
# Deixar rodando...
```

**Terminal 2 - Backend**
```bash
cd account-management-api
python -m uvicorn src.main:app --reload
# Deixar rodando...
```

**Terminal 3 - Comandos/Testes**
```bash
# Usar para testar com curl ou rodar scripts
```

## 📊 Verificação de Status

| Componente | URL | Status | O que fazer se cair |
|-----------|-----|--------|-------------------|
| Frontend | http://localhost:5173 | Deve acessar | `npm run dev` em NomNom/ |
| Backend | http://localhost:8000 | Deve responder | `python -m uvicorn src.main:app --reload` |
| API Docs | http://localhost:8000/docs | Deve abrir | Verificar backend |
| Base de Dados | Supabase | Deve conectar | Verificar .env |

## 🐛 Se não funcionar

### Frontend não conecta ao Backend

**Erro típico:** `Error: Network Error` ou `getaddrinfo failed`

**Soluções:**
1. Verifique se backend está rodando: `http://localhost:8000`
2. Verifique se URL está correta em `src/api/client.js`
3. Verifique CORS em `account-management-api/src/main.py`
4. Reinicie ambas as aplicações

### Backend não aceita requisições

**Erro: `Cors Error`**

**Solução:** CORS já está configurado, mas se ainda tiver erro:
```python
# Em account-management-api/src/main.py
# Procure por app.add_middleware(CORSMiddleware, ...)
# E verifique se "http://localhost:5173" está em allow_origins
```

### npm install falha

**Erro:** `npm ERR! code ERESOLVE`

**Solução:**
```bash
npm install --legacy-peer-deps
```

### Port 5173 já está em uso

**Erro:** `Port 5173 is already in use`

**Solução:**
```bash
npm run dev -- --port 5174
# Ou feche a aplicação anterior
```

### Port 8000 já está em uso

**Erro:** `Address already in use`

**Solução:**
```bash
# Windows - Kill processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Ou use outra porta
python -m uvicorn src.main:app --port 8001 --reload
```

## 📱 Acessar de outro Computador

### Permitir acesso externo

**Frontend:**
```bash
npm run dev -- --host
# Acesse em: http://<seu-ip>:5173
```

**Backend:**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
# Acesse em: http://<seu-ip>:8000
```

**Mas deixe em localhost para desenvolvimento seguro!**

## 🚀 Build para Produção

### Frontend

```bash
cd NomNom
npm run build
# Gera pasta dist/ pronta para deploy
```

### Backend

```bash
# Não precisa build, apenas deploy o código
# Usar Gunicorn ou Waitress em produção
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 src.main:app
```

## 📝 Checklist de Configuração

- [ ] Node.js 18+ instalado
- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`npm install`)
- [ ] Backend configurado com .env
- [ ] Backend rodando em :8000
- [ ] Frontend rodando em :5173
- [ ] Página "Buscar Usuário" acessível
- [ ] Lista de usuários carrega
- [ ] Pode buscar e editar usuários

## 💾 Salvar Trabalho

### Antes de parar de trabalhar

1. Commit no Git
```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

2. Anote os IDs de teste para próxima vez

3. Salve dados importantes do Supabase

## 🎯 Próximas Ações

Agora que tem tudo rodando:

1. ✅ Testar todos os endpoints
2. 📖 Ler BUSCA_USUARIOS_README.md (no NomNom/)
3. 🎨 Personalizar estilos (style.css)
4. ➕ Adicionar criar usuário no frontend
5. 🔐 Integrar login/logout
6. 🚀 Deploy em produção

---

**Tudo pronto?** Acesse `http://localhost:5173` e comece! 🎉
