<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <h1>Complete seu Perfil</h1>
        <p class="subtitle">Precisamos de algumas informações para personalizar sua experiência</p>
      </div>

      <form @submit.prevent="handleSubmit" class="profile-form">
        <!-- Nome -->
        <div class="form-group">
          <label for="nome">Nome Completo *</label>
          <input
            id="nome"
            v-model="formData.nome"
            type="text"
            placeholder="Digite seu nome completo"
            required
          />
        </div>

        <!-- Data de Nascimento -->
        <div class="form-group">
          <label for="data_nascimento">Data de Nascimento *</label>
          <input
            id="data_nascimento"
            v-model="formData.data_nascimento"
            type="date"
            required
          />
        </div>

        <!-- Altura -->
        <div class="form-group">
          <label for="altura">Altura (cm) *</label>
          <input
            id="altura"
            v-model.number="formData.altura"
            type="number"
            min="50"
            max="300"
            step="0.1"
            placeholder="Digite sua altura em centímetros"
            required
          />
        </div>

        <!-- Peso -->
        <div class="form-group">
          <label for="peso">Peso (kg) *</label>
          <input
            id="peso"
            v-model.number="formData.peso"
            type="number"
            min="20"
            max="500"
            step="0.1"
            placeholder="Digite seu peso em quilogramas"
            required
          />
        </div>

        <!-- Sexo -->
        <div class="form-group">
          <label for="sexo">Sexo *</label>
          <select id="sexo" v-model="formData.sexo" required>
            <option value="" disabled>Selecione seu sexo</option>
            <option v-for="opt in sexoOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <!-- Tipo de Alimentação -->
        <div class="form-group">
          <label for="alimentacao">Alimentação *</label>
          <select id="alimentacao" v-model="formData.alimentacao" required>
            <option value="" disabled>Selecione seu tipo de alimentação</option>
            <option v-for="opt in alimentacaoOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <!-- Error/Success Messages -->
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <div v-if="success" class="alert alert-success">
          {{ success }}
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading">Salvando...</span>
          <span v-else>Completar Perfil</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../../api/client';

const router = useRouter();

const formData = ref({
  nome: '',
  data_nascimento: '',
  altura: null,
  peso: null,
  sexo: '',
  alimentacao: ''
});

const loading = ref(false);
const error = ref(null);
const success = ref(null);
const alimentacaoOptions = ref([]);
const sexoOptions = ref([]);

onMounted(async () => {
  // Pegar nome e email do usuário do localStorage
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  if (user.name) {
    formData.value.nome = user.name;
  }
  
  // Verificar se usuário está autenticado
  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  // Buscar opções de enums da API
  try {
    const response = await apiClient.get('/api/v1/utilizador/options/enums');
    alimentacaoOptions.value = response.data.alimentacao;
    sexoOptions.value = response.data.sexo;
  } catch (err) {
    console.error('Erro ao buscar opções:', err);
    error.value = 'Erro ao carregar opções de formulário.';
  }
});

const handleSubmit = async () => {
  error.value = null;
  success.value = null;

  // Validações
  if (!formData.value.nome || !formData.value.data_nascimento || !formData.value.altura || 
      !formData.value.peso || !formData.value.sexo || !formData.value.alimentacao) {
    error.value = 'Por favor, preencha todos os campos';
    return;
  }

  if (formData.value.altura < 50 || formData.value.altura > 300) {
    error.value = 'Altura deve estar entre 50 e 300 cm';
    return;
  }

  if (formData.value.peso < 20 || formData.value.peso > 500) {
    error.value = 'Peso deve estar entre 20 e 500 kg';
    return;
  }

  loading.value = true;

  try {
    // Pegar email do usuário
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!user.email) {
      error.value = 'Email do usuário não encontrado. Faça login novamente.';
      loading.value = false;
      return;
    }

    const profileData = {
      email: user.email,
      nome: formData.value.nome,
      data_nascimento: formData.value.data_nascimento,
      altura: formData.value.altura,
      peso: formData.value.peso,
      sexo: formData.value.sexo,
      alimentacao: formData.value.alimentacao
    };

    const response = await apiClient.post('/api/v1/utilizador/', profileData);

    success.value = 'Perfil completado com sucesso! Redirecionando...';
    
    // Atualizar informação no localStorage
    localStorage.setItem('profile_complete', 'true');
    
    // Redirecionar após 1.5 segundos
    setTimeout(() => {
      router.push('/recipes');
    }, 1500);

  } catch (err) {
    console.error('Erro ao salvar perfil:', err);
    if (err.response?.status === 409) {
      error.value = 'Perfil já existe. Redirecionando...';
      setTimeout(() => {
        router.push('/recipes');
      }, 1500);
    } else {
      error.value = err.response?.data?.detail || 'Erro ao salvar perfil. Tente novamente.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700&display=swap');

.profile-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1ab394 0%, #ffffff 100%);
  padding: 2rem;
  font-family: 'Nunito Sans', sans-serif;
}

.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 3rem;
  width: 100%;
  max-width: 600px;
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

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
}

.profile-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 0.95rem;
  margin: 0;
}

.profile-form {
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
  color: #2c3e50;
  font-size: 0.95rem;
}

.form-group input,
.form-group select {
  padding: 0.875rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: 'Nunito Sans', sans-serif;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #1ab394;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1);
}

.form-group select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%232c3e50' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.875rem center;
  padding-right: 2.5rem;
}

.alert {
  padding: 0.875rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
}

.alert-error {
  background-color: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

.alert-success {
  background-color: #efe;
  color: #3c3;
  border: 1px solid #cfc;
}

.btn-submit {
  background: linear-gradient(135deg, #1ab394, #108c73);
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  font-family: 'Nunito Sans', sans-serif;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(26, 179, 148, 0.3);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .profile-card {
    padding: 2rem;
  }

  .profile-header h1 {
    font-size: 1.75rem;
  }
}
</style>
