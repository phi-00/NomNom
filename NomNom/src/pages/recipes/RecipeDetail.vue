<template>
  <div class="recipe-detail-container">
    <router-link to="/recipes" class="back-link">← Voltar</router-link>
    
    <div v-if="loading" class="loading">Carregando receita...</div>
    
    <div v-else-if="error" class="error-message">
      ⚠️ {{ error }}
    </div>
    
    <div v-else-if="recipe" class="recipe-detail">
      <div class="recipe-header">
        <img :src="recipe.imagem || recipe.image" :alt="recipe.nome || recipe.name" class="recipe-image" />
        
        <div class="recipe-info">
          <h1>{{ recipe.nome || recipe.name }}</h1>
          
          <div class="recipe-stats">
            <div class="stat">
              <span class="stat-label">⏱️ Tempo</span>
              <span class="stat-value">{{ recipe.tempo_preparacao || recipe.time }} min</span>
            </div>
            <div class="stat">
              <span class="stat-label">🍽️ Porções</span>
              <span class="stat-value">{{ recipe.porcoes || recipe.servings || 4 }}</span>
            </div>
            <div class="stat">
              <span class="stat-label">📊 Dificuldade</span>
              <span class="stat-value difficulty" :class="recipe.dificuldade">{{ recipe.dificuldade || 'Normal' }}</span>
            </div>
            <div class="stat" v-if="recipe.categoria">
              <span class="stat-label">🏷️ Categoria</span>
              <span class="stat-value">{{ recipe.categoria }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Seção de Ingredientes -->
      <div class="recipe-ingredientes">
        <h2>🥘 Ingredientes</h2>
        
        <!-- Resumo de Calorias -->
        <div v-if="recipe.calorias_totais" class="calorias-resumo">
          <div class="caloria-box">
            <span class="caloria-label">Calorias Totais</span>
            <span class="caloria-valor">{{ Math.round(recipe.calorias_totais) }} kcal</span>
          </div>
          <div class="caloria-box">
            <span class="caloria-label">Por Porção</span>
            <span class="caloria-valor">{{ Math.round(recipe.calorias_totais / (recipe.porcoes || recipe.servings || 4)) }} kcal</span>
          </div>
        </div>

        <!-- Lista de Ingredientes -->
        <div v-if="recipe.ingredientes && recipe.ingredientes.length > 0" class="ingredientes-lista">
          <div v-for="ing in recipe.ingredientes" :key="ing.id" class="ingrediente-item">
            <div class="ingrediente-info">
              <span class="ingrediente-nome">{{ ing.nome }}</span>
              <span class="ingrediente-quantidade">{{ ing.quantidade }} {{ ing.unidade }}</span>
            </div>
            <div class="ingrediente-calorias">
              <span class="calorias-valor">{{ Math.round(ing.quantidade * ing.calorias) }} kcal</span>
              <span class="calorias-per-unit">({{ ing.calorias }} por {{ ing.unidade }})</span>
            </div>
          </div>
        </div>
        <p v-else class="empty-message">
          Nenhum ingrediente disponível
        </p>
      </div>

      <div class="recipe-steps">
        <h2>📝 Passos da Receita</h2>
        <div class="steps-content">
          <p v-if="recipe.descricao" class="steps-text">
            {{ recipe.descricao }}
          </p>
          <p v-else class="empty-message">
            Nenhuma descrição disponível
          </p>
        </div>
      </div>

      <div v-if="recipe.num_etapas" class="recipe-footer">
        <p>Total de {{ recipe.num_etapas }} etapas</p>
      </div>
    </div>
    
    <div v-else class="not-found">
      Receita não encontrada
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '../../api/client';

const route = useRoute();
const router = useRouter();

const recipe = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // Buscar a receita com ingredientes e calorias
    const recipeId = route.params.id;
    const response = await apiClient.get(`/api/v1/receitas/${recipeId}`);
    recipe.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao buscar receita';
    console.error('Erro ao buscar receita:', err);
    setTimeout(() => {
      router.push('/recipes');
    }, 2000);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.recipe-detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Nunito Sans', sans-serif;
  color: var(--text-primary);
}

.back-link {
  display: inline-block;
  margin-bottom: 2rem;
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s;
}

.back-link:hover {
  color: #0d8659;
  margin-left: -0.5rem;
}

.loading,
.not-found,
.error-message {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.error-message {
  background: #fee;
  color: #c33;
  border: 1px solid #fcc;
  border-radius: 8px;
  margin: 1rem 0;
}

.recipe-detail {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.recipe-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
}

.recipe-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
}

.recipe-info h1 {
  margin: 0 0 1.5rem 0;
  font-size: 2rem;
  color: white;
}

.recipe-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat {
  background: rgba(255, 255, 255, 0.2);
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  opacity: 0.9;
  font-weight: 500;
}

.stat-value {
  font-size: 1.3rem;
  font-weight: 700;
  text-transform: uppercase;
}

.stat-value.difficulty {
  font-size: 1rem;
  text-transform: capitalize;
}

/* Estilos para Ingredientes */
.recipe-ingredientes {
  padding: 2rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.recipe-ingredientes h2 {
  color: var(--text-primary);
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  border-bottom: 3px solid var(--accent-color);
  padding-bottom: 0.5rem;
}

.calorias-resumo {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.caloria-box {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(26, 179, 148, 0.2);
}

.caloria-label {
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 500;
  text-transform: uppercase;
}

.caloria-valor {
  font-size: 1.8rem;
  font-weight: 700;
}

.ingredientes-lista {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ingrediente-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1.5rem;
  padding: 1rem;
  background: var(--bg-card);
  border-radius: 8px;
  border-left: 4px solid var(--accent-color);
  align-items: center;
}

.ingrediente-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.ingrediente-nome {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1.05rem;
  text-transform: capitalize;
}

.ingrediente-quantidade {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
}

.ingrediente-calorias {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  text-align: right;
}

.calorias-valor {
  color: var(--accent-color);
  font-weight: 700;
  font-size: 1.1rem;
}

.calorias-per-unit {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.recipe-steps {
  padding: 2rem;
  border-top: 1px solid var(--border-color);
}

.recipe-steps h2 {
  color: var(--text-primary);
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  border-bottom: 3px solid var(--accent-color);
  padding-bottom: 0.5rem;
}

.steps-content {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid var(--accent-color);
}

.steps-text {
  color: var(--text-primary);
  line-height: 1.8;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.empty-message {
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
}

.recipe-footer {
  padding: 1rem 2rem;
  background: var(--bg-secondary);
  text-align: center;
  color: var(--text-secondary);
  font-weight: 500;
}

@media (max-width: 768px) {
  .recipe-detail-container {
    padding: 1rem;
  }

  .recipe-header {
    grid-template-columns: 1fr;
  }

  .recipe-image {
    height: 250px;
  }

  .recipe-stats {
    grid-template-columns: 1fr;
  }

  .recipe-info h1 {
    font-size: 1.5rem;
  }

  .recipe-steps {
    padding: 1.5rem;
  }

  .recipe-ingredientes {
    padding: 1.5rem;
  }

  .calorias-resumo {
    grid-template-columns: 1fr;
  }

  .ingrediente-item {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .ingrediente-calorias {
    text-align: left;
  }
}
</style>
