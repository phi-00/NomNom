# 🔗 Integração Frontend - Account Management API

## Conexão com o Frontend Vue.js

Se você tem um projeto Vue.js no `NomNom/`, aqui está como conectar:

### 1️⃣ Instalação de Dependências (Vue.js)

```bash
cd NomNom/
npm install axios
```

### 2️⃣ Criação de Cliente API

Crie um arquivo `src/api/client.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Adicionar interceptor para incluir token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

### 3️⃣ Criar Composable para Contas

Crie `src/composables/useAccounts.js`:

```javascript
import { ref } from 'vue';
import apiClient from '@/api/client';

export function useAccounts() {
  const accounts = ref([]);
  const current = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const createAccount = async (name, email, password) => {
    loading.value = true;
    try {
      const response = await apiClient.post('/accounts/', {
        name,
        email,
        password,
      });
      current.value = response.data;
      error.value = null;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao criar conta';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const listAccounts = async (limit = 10, offset = 0) => {
    loading.value = true;
    try {
      const response = await apiClient.get('/accounts/', {
        params: { limit, offset },
      });
      accounts.value = response.data;
      error.value = null;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao listar contas';
    } finally {
      loading.value = false;
    }
  };

  const getAccount = async (accountId) => {
    loading.value = true;
    try {
      const response = await apiClient.get(`/accounts/${accountId}`);
      current.value = response.data;
      error.value = null;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Conta não encontrada';
    } finally {
      loading.value = false;
    }
  };

  const updateAccount = async (accountId, name, email) => {
    loading.value = true;
    try {
      const response = await apiClient.put(`/accounts/${accountId}`, {
        name,
        email,
      });
      current.value = response.data;
      error.value = null;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao atualizar conta';
    } finally {
      loading.value = false;
    }
  };

  const deleteAccount = async (accountId) => {
    loading.value = true;
    try {
      await apiClient.delete(`/accounts/${accountId}`);
      accounts.value = accounts.value.filter((a) => a.id !== accountId);
      current.value = null;
      error.value = null;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao deletar conta';
    } finally {
      loading.value = false;
    }
  };

  return {
    accounts,
    current,
    loading,
    error,
    createAccount,
    listAccounts,
    getAccount,
    updateAccount,
    deleteAccount,
  };
}
```

### 4️⃣ Criar Composable para Autenticação

Crie `src/composables/useAuth.js`:

```javascript
import { ref } from 'vue';
import apiClient from '@/api/client';

export function useAuth() {
  const user = ref(null);
  const token = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const login = async (email, password) => {
    loading.value = true;
    try {
      const response = await apiClient.post('/auth/login', {
        email,
        password,
      });
      
      token.value = response.data.access_token;
      user.value = response.data.user;
      
      // Salvar token no localStorage
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      
      error.value = null;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao fazer login';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    loading.value = true;
    try {
      await apiClient.post('/auth/logout');
      
      token.value = null;
      user.value = null;
      
      // Limpar localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      error.value = null;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao fazer logout';
    } finally {
      loading.value = false;
    }
  };

  const getCurrentUser = async () => {
    loading.value = true;
    try {
      const response = await apiClient.get('/auth/me');
      user.value = response.data;
      error.value = null;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Não autenticado';
      logout();
    } finally {
      loading.value = false;
    }
  };

  const restoreToken = () => {
    const savedToken = localStorage.getItem('access_token');
    if (savedToken) {
      token.value = savedToken;
    }
  };

  return {
    user,
    token,
    loading,
    error,
    login,
    logout,
    getCurrentUser,
    restoreToken,
  };
}
```

### 5️⃣ Usar em Componentes Vue

Exemplo de componente para criar conta:

```vue
<template>
  <div class="create-account">
    <h2>Criar Conta</h2>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>Nome:</label>
        <input v-model="form.name" type="text" required />
      </div>
      
      <div class="form-group">
        <label>Email:</label>
        <input v-model="form.email" type="email" required />
      </div>
      
      <div class="form-group">
        <label>Senha:</label>
        <input v-model="form.password" type="password" required />
      </div>
      
      <button type="submit" :disabled="loading">
        {{ loading ? 'Criando...' : 'Criar Conta' }}
      </button>
    </form>
    
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="current" class="success">Conta criada: {{ current.name }}</p>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useAccounts } from '@/composables/useAccounts';

const { createAccount, current, loading, error } = useAccounts();

const form = reactive({
  name: '',
  email: '',
  password: '',
});

const handleSubmit = async () => {
  try {
    await createAccount(form.name, form.email, form.password);
    // Limpar formulário
    form.name = '';
    form.email = '';
    form.password = '';
  } catch (err) {
    console.error('Erro:', err);
  }
};
</script>
```

### 6️⃣ Configurar CORS (Production)

No arquivo `src/main.py`, faça ajustes para sua URL do frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

# Para desenvolvimento
origins = [
    "http://localhost:5173",  # Vue dev server padrão (Vite)
    "http://localhost:3000",  # Alternativo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7️⃣ Executar Ambos

**Terminal 1 - Backend:**
```bash
cd account-management-api
python -m uvicorn src.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd NomNom
npm run dev
```

## 🔄 Fluxo de Comunicação

```
Vue.js App
    ↓
apiClient (Axios)
    ↓
FastAPI Backend (http://localhost:8000)
    ↓
Supabase Auth
    ↓
Supabase Database
```

## 🛡️ Segurança

- ✅ Token JWT armazenado no localStorage
- ✅ Interceptor automático adiciona token
- ✅ Logout limpa token
- ✅ CORS protegido
- ✅ Validação no backend

## 📌 Variáveis de Ambiente Frontend

Crie `.env` no NomNom/:

```env
VITE_API_BASE_URL=http://localhost:8000
```

E use em `src/api/client.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

## 🐛 Troubleshooting

### CORS Error
- Verifique se o backend está rodando
- Ajuste `allow_origins` em `src/main.py`

### Token não persiste
- Verifique localStorage no DevTools
- Verifique se o token é salvo após login

### 404 Not Found
- Verifique a URL correta em apiClient
- Verifique se o endpoint existe em `/docs`

---

Pronto! Agora você tem um sistema completo de contas! 🚀
