<template>
  <section class="my-recipes">
    <h1>My Recipes</h1>
    
    <!-- Search Bar -->
    <div class="search-bar-wrapper">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search your recipes..." 
        class="search-input-small"
        @input="filterBySearch"
      />
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
    <div v-else-if="myRecipes.length === 0" class="no-recipes">No recipes found</div>
    <div v-else class="recipes-grid">
      <div class="recipe-card" v-for="recipe in myRecipes" :key="recipe.id" @click="goToRecipe(recipe.id)">
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
import { onMounted, computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRecipes } from '../../composables/useRecipes';

const router = useRouter();
const { minhasReceitas, loading, error, fetchMinhasReceitas } = useRecipes();
const searchQuery = ref('');

const myRecipes = computed(() => {
  const recipes = minhasReceitas.value || [];
  
  // Filter by search query
  if (searchQuery.value.trim() === '') {
    return recipes;
  }
  
  const query = searchQuery.value.toLowerCase();
  return recipes.filter(recipe => {
    const name = (recipe.nome || recipe.name || '').toLowerCase();
    return name.includes(query);
  });
});

onMounted(async () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  await fetchMinhasReceitas(user.email || null);
});

const filterBySearch = () => {
  // The computed property myRecipes will automatically filter based on searchQuery
};

const goToRecipe = (recipeId) => {
  router.push(`/recipes/${recipeId}`);
};
</script>

<style scoped>
.my-recipes {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
  color: var(--text-primary);
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
  color: #1ab394;
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

.search-bar-wrapper {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 2rem;
}

.search-input-small {
  width: 350px;
  padding: 0.85rem 1.1rem;
  font-size: 1rem;
  border: 2px solid rgba(26, 179, 148, 0.3);
  border-radius: 10px;
  background-color: var(--input-bg);
  color: var(--text-primary);
  transition: all 0.3s ease;
  font-family: 'Nunito Sans', sans-serif;
}

.search-input-small:focus {
  outline: none;
  border-color: #1ab394;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1);
}

.search-input-small::placeholder {
  color: var(--text-secondary);
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
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, rgba(26, 179, 148, 0.85) 0%, rgba(21, 151, 109, 0.85) 100%) !important;
  color: white !important;
  padding: 6px 12px !important;
  border-radius: 50px !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  white-space: nowrap !important;
  box-shadow: 0 2px 8px rgba(26, 179, 148, 0.3) !important;
}
</style>
