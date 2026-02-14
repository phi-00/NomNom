<script setup>
import { onMounted } from 'vue';
import { useIngredients } from '../composables/useIngredients';

const { ingredientes, loading, error, fetchIngredientes } = useIngredients();

onMounted(() => {
  fetchIngredientes();
});
</script>

<template>
  <div class="ingredientes-container">
    <div class="header">
      <h1>🍎 Ingredientes - Nome e Calorias</h1>
      <p class="subtitle">Visualize todos os ingredientes cadastrados no sistema</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando ingredientes...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">❌</div>
      <h2>Erro ao carregar</h2>
      <p>{{ error }}</p>
      <button @click="fetchIngredientes" class="retry-button">
        Tentar novamente
      </button>
    </div>

    <div v-else-if="ingredientes.length > 0" class="success-state">
      <div class="info-box">
        <span class="info-label">Total de ingredientes:</span>
        <span class="info-value">{{ ingredientes.length }}</span>
      </div>

      <div class="ingredientes-grid">
        <div v-for="(ingrediente, index) in ingredientes" :key="ingrediente.id || index" class="ingrediente-card">
          <div class="ingrediente-number">{{ index + 1 }}</div>
          <div class="ingrediente-content">
            <h3>{{ ingrediente.nome }}</h3>
            <div class="ingrediente-calorias">
              <span class="caloria-icon">🔥</span>
              <span class="caloria-value">{{ ingrediente.calorias }}</span>
              <span class="caloria-unit">kcal</span>
            </div>
          </div>
        </div>
      </div>

      <div class="ingredientes-table">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Nome</th>
              <th>Calorias (kcal)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(ingrediente, index) in ingredientes" :key="ingrediente.id || index">
              <td class="index-cell">{{ index + 1 }}</td>
              <td class="nome-cell">{{ ingrediente.nome }}</td>
              <td class="calorias-cell">
                <span class="caloria-badge">{{ ingrediente.calorias }} kcal</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📭</div>
      <h2>Nenhum ingrediente encontrado</h2>
      <p>A tabela <strong>Ingrediente</strong> está vazia.</p>
      <p class="hint">💡 Adicione alguns ingredientes na tabela do Supabase!</p>
    </div>
  </div>
</template>

<style scoped>
.ingredientes-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #333;
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

/* Estados de Carregamento */
.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  text-align: center;
  gap: 1rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-state p,
.error-state p,
.empty-state p {
  color: #666;
  font-size: 1rem;
}

.error-icon,
.empty-icon {
  font-size: 3rem;
}

.error-state h2,
.empty-state h2 {
  color: #333;
  margin: 0;
}

.hint {
  background: #f0f7ff;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  margin-top: 1rem;
  font-weight: 500;
}

.retry-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.retry-button:hover {
  background: #5568d3;
}

/* Estado de Sucesso */
.success-state {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.info-label {
  font-size: 1rem;
  font-weight: 500;
}

.info-value {
  font-size: 1.5rem;
  font-weight: bold;
}

/* Grid de Ingredientes */
.ingredientes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  animation: slideUp 0.3s ease-in;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ingrediente-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.ingrediente-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.ingrediente-number {
  background: #f0f0f0;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #667eea;
  font-size: 0.9rem;
}

.ingrediente-content {
  width: 100%;
}

.ingrediente-content h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1rem;
  word-break: break-word;
}

.ingrediente-calorias {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  background: #fff3e0;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  border: 1px solid #ffb74d;
}

.caloria-icon {
  font-size: 1rem;
}

.caloria-value {
  font-weight: bold;
  color: #f57c00;
  font-size: 1.1rem;
}

.caloria-unit {
  color: #666;
  font-size: 0.85rem;
}

/* Tabela */
.columns-table {
  overflow-x: auto;
  margin-top: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

thead th {
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.95rem;
}

tbody tr {
  border-bottom: 1px solid #e0e0e0;
  transition: background 0.2s;
}

tbody tr:hover {
  background: #f9f9f9;
}

tbody tr:last-child {
  border-bottom: none;
}

td {
  padding: 1rem;
  color: #333;
}

.index-cell {
  font-weight: 600;
  color: #667eea;
  width: 50px;
  text-align: center;
}

.nome-cell {
  font-weight: 500;
  color: #333;
  font-size: 1rem;
}

.calorias-cell {
  text-align: center;
  width: 150px;
}

.caloria-badge {
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  display: inline-block;
  font-size: 0.9rem;
  box-shadow: 0 2px 4px rgba(245, 124, 0, 0.3);
}

/* Responsivo */
@media (max-width: 768px) {
  .ingredientes-container {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .ingredientes-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 0.75rem;
  }

  table {
    font-size: 0.9rem;
  }

  thead th,
  td {
    padding: 0.75rem 0.5rem;
  }

  .caloria-badge {
    padding: 0.3rem 0.8rem;
    font-size: 0.85rem;
  }
}
</style>
