<template>
  <div class="recipe-detail-container">
    <router-link to="/recipes" class="back-link">← Voltar</router-link>
    
    <div v-if="loading" class="loading">Carregando receita...</div>
    
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

      <div class="recipe-steps">
        <h2>Passos da Receita</h2>
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
import { useRecipes } from '../../composables/useRecipes';

const route = useRoute();
const router = useRouter();
const { todasReceitas, fetchTodasReceitas } = useRecipes();

const recipe = ref(null);
const loading = ref(true);

onMounted(async () => {
  loading.value = true;
  
  // Buscar todas as receitas
  await fetchTodasReceitas();
  
  // Encontrar a receita pelo ID
  const recipeId = route.params.id;
  recipe.value = todasReceitas.value.find(r => r.id === parseInt(recipeId));
  
  loading.value = false;
  
  if (!recipe.value) {
    setTimeout(() => {
      router.push('/recipes');
    }, 2000);
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
.not-found {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
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
}
</style>
