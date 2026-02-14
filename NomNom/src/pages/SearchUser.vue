<template>
  <div class="search-user-container">
    <div class="search-section">
      <h1>Buscar Usuário</h1>
      
      <div class="search-form">
        <input
          v-model="searchId"
          type="text"
          placeholder="Digite o ID do usuário"
          @keyup.enter="handleSearch"
          class="search-input"
        />
        <button 
          @click="handleSearch" 
          :disabled="loading || !searchId.trim()"
          class="search-button"
        >
          {{ loading ? 'Buscando...' : 'Buscar' }}
        </button>
      </div>

      <div v-if="error" class="error-message">
        <p>❌ {{ error }}</p>
      </div>

      <div v-if="currentUser" class="user-card">
        <div class="card-header">
          <h2>{{ currentUser.name }}</h2>
          <span class="id-badge">{{ currentUser.id }}</span>
        </div>
        
        <div class="card-content">
          <div class="info-row">
            <label>Email:</label>
            <span>{{ currentUser.email }}</span>
          </div>
          
          <div class="info-row">
            <label>Criado em:</label>
            <span>{{ formatDate(currentUser.created_at) }}</span>
          </div>
        </div>

        <div class="card-actions">
          <button @click="handleDelete" class="btn-delete">Deletar Usuário</button>
          <button @click="showEditForm = !showEditForm" class="btn-edit">
            {{ showEditForm ? 'Cancelar' : 'Editar' }}
          </button>
        </div>

        <div v-if="showEditForm" class="edit-form">
          <h3>Editar Usuário</h3>
          <div class="form-group">
            <label>Nome:</label>
            <input v-model="editForm.name" type="text" />
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input v-model="editForm.email" type="email" />
          </div>
          <button @click="handleUpdate" class="btn-save">Salvar Alterações</button>
        </div>
      </div>
    </div>

    <div class="list-section">
      <h2>Listar Usuários</h2>
      
      <button 
        @click="handleListUsers"
        :disabled="loading"
        class="list-button"
      >
        {{ loading ? 'Carregando...' : 'Carregar Usuários' }}
      </button>

      <div v-if="users.length > 0" class="users-list">
        <div v-for="user in users" :key="user.id" class="user-item">
          <div class="user-info">
            <h3>{{ user.name }}</h3>
            <p>{{ user.email }}</p>
          </div>
          <button @click="searchId = user.id; handleSearch()" class="btn-view">
            Ver Detalhes
          </button>
        </div>
      </div>

      <div v-else-if="users.length === 0 && !loading" class="empty-state">
        <p>Nenhum usuário para listar</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUsers } from '@/composables/useUsers';

const { users, currentUser, loading, error, getUser, listUsers, deleteUser, updateUser } = useUsers();

const searchId = ref('');
const showEditForm = ref(false);
const editForm = ref({
  name: '',
  email: '',
});

const handleSearch = async () => {
  if (!searchId.value.trim()) {
    return;
  }
  try {
    await getUser(searchId.value);
  } catch (err) {
    console.error('Erro na busca:', err);
  }
};

const handleListUsers = async () => {
  try {
    await listUsers();
  } catch (err) {
    console.error('Erro ao listar:', err);
  }
};

const handleDelete = async () => {
  if (confirm('Tem certeza que deseja deletar este usuário?')) {
    try {
      await deleteUser(currentUser.value.id);
      searchId.value = '';
      alert('Usuário deletado com sucesso!');
    } catch (err) {
      console.error('Erro ao deletar:', err);
    }
  }
};

const handleUpdate = async () => {
  try {
    await updateUser(
      currentUser.value.id,
      editForm.value.name,
      editForm.value.email
    );
    showEditForm.value = false;
    alert('Usuário atualizado com sucesso!');
  } catch (err) {
    console.error('Erro ao atualizar:', err);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script>

<style scoped>
.search-user-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  border-radius: 10px;
}

h1 {
  color: #fff;
  margin-bottom: 1.5rem;
  font-size: 2rem;
}

h2 {
  color: #fff;
  margin-bottom: 1rem;
}

.search-section,
.list-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.search-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.search-button,
.list-button {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.search-button:hover:not(:disabled),
.list-button:hover:not(:disabled) {
  background: #5568d3;
}

.search-button:disabled,
.list-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 5px;
  margin-bottom: 1rem;
  border-left: 4px solid #c33;
}

.user-card {
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 1rem;
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: white;
}

.id-badge {
  background: rgba(255, 255, 255, 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-family: monospace;
}

.card-content {
  padding: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row label {
  font-weight: 600;
  color: #333;
}

.info-row span {
  color: #666;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.btn-delete,
.btn-edit,
.btn-save,
.btn-view {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-delete {
  background: #ff6b6b;
  color: white;
}

.btn-delete:hover {
  background: #ee5a52;
}

.btn-edit {
  background: #ffa500;
  color: white;
}

.btn-edit:hover {
  background: #e69500;
}

.btn-save {
  background: #51cf66;
  color: white;
  width: 100%;
}

.btn-save:hover {
  background: #40c057;
}

.btn-view {
  background: #667eea;
  color: white;
  padding: 0.5rem 1rem;
  flex: 0;
}

.btn-view:hover {
  background: #5568d3;
}

.edit-form {
  padding: 1rem;
  background: #fff9e6;
  border-top: 1px solid #e0e0e0;
  border-radius: 0 0 8px 8px;
}

.edit-form h3 {
  margin-top: 0;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.user-info h3 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.user-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #999;
  font-style: italic;
}

@media (max-width: 768px) {
  .search-user-container {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .card-actions {
    flex-direction: column;
  }

  .user-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .btn-view {
    width: 100%;
  }
}
</style>
