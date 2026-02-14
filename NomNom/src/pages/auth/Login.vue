<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>🍔 Bem-vindo de Volta!</h1>
        <p>Entre na sua conta para continuar</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            placeholder="seu@email.com"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Senha</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            placeholder="Digite sua senha"
            required
            :disabled="loading"
          />
        </div>

        <div v-if="error" class="error-message">
          ❌ {{ error }}
        </div>

        <div v-if="success" class="success-message">
          ✅ {{ success }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="loading">Entrando...</span>
          <span v-else>Entrar</span>
        </button>
      </form>

      <div class="auth-footer">
        <p>Não tem uma conta?</p>
        <router-link to="/register" class="link">Criar Conta</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../../api/client';

const router = useRouter();

const formData = ref({
  email: '',
  password: ''
});

const loading = ref(false);
const error = ref(null);
const success = ref(null);

const handleLogin = async () => {
  error.value = null;
  success.value = null;

  if (!formData.value.email || !formData.value.password) {
    error.value = 'Preencha todos os campos';
    return;
  }

  loading.value = true;

  try {
    const response = await apiClient.post('/api/v1/auth/login', {
      email: formData.value.email,
      password: formData.value.password
    });

    success.value = 'Login realizado com sucesso! Redirecionando...';
    
    // Salvar token e dados do usuário
    if (response.data.session?.access_token) {
      localStorage.setItem('access_token', response.data.session.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    // Redirecionar após 1 segundo
    setTimeout(() => {
      router.push('/recipes');
    }, 1000);

  } catch (err) {
    console.error('Erro ao fazer login:', err);
    error.value = err.response?.data?.detail || 'Email ou senha incorretos';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.auth-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 3rem;
  width: 100%;
  max-width: 450px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 2rem;
}

.auth-header p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.875rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 0.875rem;
  border-radius: 8px;
  border-left: 4px solid #c62828;
  font-size: 0.9rem;
}

.success-message {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 0.875rem;
  border-radius: 8px;
  border-left: 4px solid #2e7d32;
  font-size: 0.9rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
}

.auth-footer p {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .auth-container {
    padding: 1rem;
  }

  .auth-card {
    padding: 2rem 1.5rem;
  }

  .auth-header h1 {
    font-size: 1.5rem;
  }
}
</style>
