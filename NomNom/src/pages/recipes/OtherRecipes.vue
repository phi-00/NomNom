<template>
  <section class="other-recipes">
    <h1>Other Recipes</h1>
    <div v-if="loading" class="loading">Loading recipes...</div>
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
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useRecipes } from '../../composables/useRecipes';

const router = useRouter();
const { outrasReceitas, loading, error, fetchOutrasReceitas } = useRecipes();

const otherRecipes = computed(() => {
  return outrasReceitas.value || [];
});

onMounted(async () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  await fetchOutrasReceitas(user.email || null);
});

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
  margin-bottom: 2rem;
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
