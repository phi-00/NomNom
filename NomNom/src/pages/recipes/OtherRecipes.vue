<template>
  <section class="other-recipes">
    <div class="header-section">
      <h1>Other Recipes</h1>
      <button class="filter-button" @click="showFilters = true">
        🔍 Filtros
      </button>
    </div>

    <!-- Filter Overlay -->
    <div v-if="showFilters" class="filter-overlay" @click.self="showFilters = false">
      <div class="filter-panel">
        <div class="filter-header">
          <h2>Filtros de Pesquisa</h2>
          <button class="close-button" @click="showFilters = false">✕</button>
        </div>
        
        <div class="filter-content">
          <!-- Only Ingredients You Have -->
          <div class="filter-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="filters.onlyMyIngredients" />
              <span>Apenas ingredientes que você tem</span>
            </label>
          </div>

          <!-- Difficulty -->
          <div class="filter-group">
            <label class="filter-label">Nível de Dificuldade</label>
            <select v-model="filters.dificuldade">
              <option value="">Todos</option>
              <option value="facil">Fácil</option>
              <option value="medio">Médio</option>
              <option value="dificil">Difícil</option>
            </select>
          </div>

          <!-- Category -->
          <div class="filter-group">
            <label class="filter-label">Categoria</label>
            <select v-model="filters.categoria">
              <option value="">Todas</option>
              <option value="padaria">Padaria</option>
              <option value="pastelaria">Pastelaria</option>
              <option value="entrada">Entrada</option>
              <option value="sopa">Sopa</option>
              <option value="prato principal">Prato Principal</option>
              <option value="bebida">Bebida</option>
            </select>
          </div>

          <!-- Cooking Type -->
          <div class="filter-group">
            <label class="filter-label">Tipo de Cozinhado</label>
            <select v-model="filters.tipo_cozinhado">
              <option value="">Todos</option>
              <option value="frito">Frito</option>
              <option value="assado">Assado</option>
              <option value="cozido">Cozido</option>
              <option value="grelhado">Grelhado</option>
              <option value="estufado">Estufado</option>
            </select>
          </div>

          <!-- Preparation Time -->
          <div class="filter-group">
            <label class="filter-label">Tempo de Preparação (minutos)</label>
            <div class="range-inputs">
              <input 
                type="number" 
                v-model.number="filters.tempo_min" 
                placeholder="Min"
                min="0"
              />
              <span>até</span>
              <input 
                type="number" 
                v-model.number="filters.tempo_max" 
                placeholder="Max"
                min="0"
              />
            </div>
          </div>

          <!-- Servings -->
          <div class="filter-group">
            <label class="filter-label">Número de Porções</label>
            <div class="range-inputs">
              <input 
                type="number" 
                v-model.number="filters.porcoes_min" 
                placeholder="Min"
                min="1"
              />
              <span>até</span>
              <input 
                type="number" 
                v-model.number="filters.porcoes_max" 
                placeholder="Max"
                min="1"
              />
            </div>
          </div>
        </div>

        <div class="filter-actions">
          <button class="clear-button" @click="clearFilters">Limpar Filtros</button>
          <button class="apply-button" @click="applyFilters">Aplicar Filtros</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-skeleton">
      <div class="skeleton-card" v-for="i in 6" :key="i">
        <div class="skeleton-image"></div>
        <div class="skeleton-title"></div>
        <div class="skeleton-text"></div>
        <div class="skeleton-meta"></div>
      </div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="otherRecipes.length === 0" class="no-recipes">No recipes found</div>
    <div v-else class="recipes-grid">
      <div class="recipe-card" v-for="recipe in otherRecipes" :key="recipe.id" @click="goToRecipe(recipe.id)">
        <img :src="recipe.imagem || recipe.image" :alt="recipe.nome || recipe.name" />
        <h3>{{ recipe.nome || recipe.name }}</h3>
        <p>{{ recipe.descricao || recipe.description }}</p>
        <div class="recipe-meta">
          <span class="time">⏱️ {{ recipe.tempo_preparacao || recipe.time }} min</span>
          <span v-if="recipe.calorias_totais" class="calories">
            🔥 {{ Math.round(recipe.calorias_totais) }} kcal
          </span>
          <div class="tags">
            <span class="tag" v-if="recipe.dificuldade">{{ recipe.dificuldade }}</span>
            <span class="tag" v-if="recipe.categoria">{{ recipe.categoria }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useRecipes } from '../../composables/useRecipes';

const router = useRouter();
const { outrasReceitas, loading, error, fetchOutrasReceitasWithFilters } = useRecipes();

const showFilters = ref(false);
const filters = ref({
  onlyMyIngredients: false,
  dificuldade: '',
  categoria: '',
  tipo_cozinhado: '',
  tempo_min: null,
  tempo_max: null,
  porcoes_min: null,
  porcoes_max: null
});

const otherRecipes = computed(() => {
  return outrasReceitas.value || [];
});

onMounted(async () => {
  await loadRecipes();
});

const loadRecipes = async () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  await fetchOutrasReceitasWithFilters(user.email || null, {});
};

const applyFilters = async () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  
  // Build filter object, only including non-empty values
  const activeFilters = {};
  
  if (filters.value.onlyMyIngredients) {
    activeFilters.onlyMyIngredients = true;
  }
  if (filters.value.dificuldade) {
    activeFilters.dificuldade = filters.value.dificuldade;
  }
  if (filters.value.categoria) {
    activeFilters.categoria = filters.value.categoria;
  }
  if (filters.value.tipo_cozinhado) {
    activeFilters.tipo_cozinhado = filters.value.tipo_cozinhado;
  }
  if (filters.value.tempo_min !== null && filters.value.tempo_min !== '') {
    activeFilters.tempo_min = filters.value.tempo_min;
  }
  if (filters.value.tempo_max !== null && filters.value.tempo_max !== '') {
    activeFilters.tempo_max = filters.value.tempo_max;
  }
  if (filters.value.porcoes_min !== null && filters.value.porcoes_min !== '') {
    activeFilters.porcoes_min = filters.value.porcoes_min;
  }
  if (filters.value.porcoes_max !== null && filters.value.porcoes_max !== '') {
    activeFilters.porcoes_max = filters.value.porcoes_max;
  }
  
  await fetchOutrasReceitasWithFilters(user.email || null, activeFilters);
  showFilters.value = false;
};

const clearFilters = () => {
  filters.value = {
    onlyMyIngredients: false,
    dificuldade: '',
    categoria: '',
    tipo_cozinhado: '',
    tempo_min: null,
    tempo_max: null,
    porcoes_min: null,
    porcoes_max: null
  };
  loadRecipes();
};

const goToRecipe = (recipeId) => {
  router.push(`/recipes/${recipeId}`);
};
</script>

<style scoped>
.other-recipes {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
  color: var(--text-primary);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filter-button {
  background: linear-gradient(135deg, var(--accent-color) 0%, #4a90e2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.filter-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Skeleton Loading */
.loading-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.skeleton-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  background: var(--bg-card);
}

.skeleton-image,
.skeleton-title,
.skeleton-text,
.skeleton-meta {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 8px;
}

@media (prefers-color-scheme: dark) {
  .skeleton-image,
  .skeleton-title,
  .skeleton-text,
  .skeleton-meta {
    background: linear-gradient(90deg, #2a2a2a 25%, #333333 50%, #2a2a2a 75%);
    background-size: 200% 100%;
  }
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton-image {
  width: 100%;
  height: 200px;
  margin-bottom: 1rem;
}

.skeleton-title {
  height: 24px;
  width: 70%;
  margin-bottom: 0.5rem;
}

.skeleton-text {
  height: 16px;
  width: 90%;
  margin-bottom: 0.5rem;
}

.skeleton-meta {
  height: 20px;
  width: 50%;
  margin-top: 0.5rem;
}

/* Filter Overlay */
.filter-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.filter-panel {
  background: #1a1a1a;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(26, 179, 148, 0.4);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid rgba(26, 179, 148, 0.3);
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
}

.filter-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: white;
}

.close-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.filter-content {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
  background: #252525;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-size: 1rem;
  color: #e0e0e0;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.filter-group select,
.filter-group input[type="number"] {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid rgba(26, 179, 148, 0.3);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
  font-family: 'Nunito Sans';
  background: #1a1a1a;
  color: #e0e0e0;
}

.filter-group select:focus,
.filter-group input[type="number"]:focus {
  outline: none;
  border-color: #1ab394;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.range-inputs input {
  flex: 1;
}

.range-inputs span {
  color: #b0b0b0;
  font-weight: 500;
}

.filter-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 2px solid rgba(26, 179, 148, 0.3);
  background: #1a1a1a;
}

.clear-button,
.apply-button {
  flex: 1;
  padding: 0.875rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.clear-button {
  background: #252525;
  color: #e0e0e0;
  border: 2px solid rgba(26, 179, 148, 0.3);
}

.clear-button:hover {
  background: #1a1a1a;
  border-color: #1ab394;
}

.apply-button {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
}

.apply-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.loading, .error, .no-recipes {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.no-recipes {
  color: var(--text-secondary);
}

h1 {
  color: var(--accent-color);
  font-size: 2.5rem;
  margin: 0;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.recipe-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  background: var(--bg-card);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  cursor: pointer;
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.recipe-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.recipe-card h3 {
  color: var(--text-primary);
  margin: 0.5rem 0;
  font-size: 1.2rem;
}

.recipe-card p {
  color: var(--text-secondary);
  margin: 0.5rem 0;
  font-size: 0.9rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.recipe-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.recipe-card .time {
  display: inline-block;
  color: var(--accent-color);
  font-weight: 500;
}

.recipe-card .calories {
  display: inline-block;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  display: inline-block;
  background-color: var(--bg-secondary);
  color: var(--accent-color);
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 0.75rem;
  font-weight: 500;
}
</style>
