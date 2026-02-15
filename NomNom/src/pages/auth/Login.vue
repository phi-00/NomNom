<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Welcome Back!</h1>
        <p>Log in to your account to continue</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            placeholder="your@email.com"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            placeholder="Enter your password"
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
          <span v-if="loading">Logging in...</span>
          <span v-else>Log In</span>
        </button>
      </form>

      <div class="auth-footer">
        <p>Don't have an account?</p>
        <router-link to="/register" class="link">Create Account</router-link>
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
    error.value = 'Please fill in all fields';
    return;
  }

  loading.value = true;

  try {
    const response = await apiClient.post('/api/v1/auth/login', {
      email: formData.value.email,
      password: formData.value.password
    });

    success.value = 'Login successful! Redirecting...';
    
    // Salvar token e dados do usuário
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    // Verificar se o perfil está completo
    const profileComplete = response.data.profile_complete || false;
    
    // Redirecionar após 1 segundo
    setTimeout(() => {
      if (!profileComplete) {
        // Se perfil não está completo, redirecionar para completar perfil
        router.push('/complete-profile');
      } else {
        // Se perfil está completo, redirecionar para home
        router.push('/home');
      }
    }, 1000);

  } catch (err) {
    console.error('Error logging in:', err);
    error.value = err.response?.data?.detail || 'Incorrect email or password';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700&display=swap');

.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-color) 0%, var(--bg-primary) 100%);
  padding: 2rem;
  font-family: 'Nunito Sans', sans-serif;
}

.auth-card {
  background: var(--bg-card);
  border-radius: 16px;
  border: 2px solid rgba(26, 179, 148, 0.2);
  box-shadow: 0 10px 30px rgba(26, 179, 148, 0.15);
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
  color: var(--text-primary);
  font-size: 2rem;
}

.auth-header p {
  margin: 0;
  color: var(--text-secondary);
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
  color: var(--text-primary);
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.875rem;
  border: 2px solid #1ab394;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: var(--input-bg);
  color: var(--text-primary);
}

.form-group input::placeholder {
  color: var(--text-secondary);
}

.form-group input:focus {
  outline: none;
  border-color: #15976d;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.2);
}

.form-group input:disabled {
  background: var(--bg-secondary);
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
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(26, 179, 148, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.auth-footer p {
  margin: 0 0 0.5rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.link {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.link:hover {
  color: var(--accent-hover);
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
