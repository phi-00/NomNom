<template>
  <section class="recipes">
    <!-- My Recipes Section -->
    <div class="recipes-section">
      <div class="section-header">
        <h2>My Recipes</h2>
        <router-link to="/recipes/myrecipes" class="see-all">see all</router-link>
      </div>
      <Carousel 
        :value="myRecipes" 
        :numVisible="3" 
        :numScroll="1" 
        :responsiveOptions="responsiveOptions"
        class="recipe-carousel"
      >
        <template #item="slotProps">
          <div class="recipe-card" @click="goToRecipe(slotProps.data.id)">
            <img :src="slotProps.data.imagem || slotProps.data.image" :alt="slotProps.data.nome || slotProps.data.name" />
            <h3>{{ slotProps.data.nome || slotProps.data.name }}</h3>
            <div class="recipe-meta">
              <span class="time">⏱️ {{ slotProps.data.tempo_preparacao || slotProps.data.time }} min</span>
              <span v-if="slotProps.data.calorias_totais" class="calories">
                🔥 {{ Math.round(slotProps.data.calorias_totais) }} kcal
              </span>
              <div class="tags">
                <span class="tag" v-if="slotProps.data.dificuldade">{{ slotProps.data.dificuldade }}</span>
                <span class="tag" v-if="slotProps.data.categoria">{{ slotProps.data.categoria }}</span>
              </div>
            </div>
          </div>
        </template>
      </Carousel>
    </div>

    <!-- Other Recipes Section -->
    <div class="recipes-section">
      <div class="section-header">
        <h2>Other Recipes</h2>
        <router-link to="/recipes/otherrecipes" class="see-all">see all</router-link>
      </div>
      <Carousel 
        :value="otherRecipes" 
        :numVisible="3" 
        :numScroll="1" 
        :responsiveOptions="responsiveOptions"
        class="recipe-carousel"
      >
        <template #item="slotProps">
          <div class="recipe-card" @click="goToRecipe(slotProps.data.id)">
            <img :src="slotProps.data.imagem || slotProps.data.image" :alt="slotProps.data.nome || slotProps.data.name" />
            <h3>{{ slotProps.data.nome || slotProps.data.name }}</h3>
            <div class="recipe-meta">
              <span class="time">⏱️ {{ slotProps.data.tempo_preparacao || slotProps.data.time }} min</span>
              <span v-if="slotProps.data.calorias_totais" class="calories">
                🔥 {{ Math.round(slotProps.data.calorias_totais) }} kcal
              </span>
              <div class="tags">
                <span class="tag" v-if="slotProps.data.dificuldade">{{ slotProps.data.dificuldade }}</span>
                <span class="tag" v-if="slotProps.data.categoria">{{ slotProps.data.categoria }}</span>
              </div>
            </div>
          </div>
        </template>
      </Carousel>
    </div>
  </section>
</template>

<script setup>
import Carousel from 'primevue/carousel';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useRecipes } from '../../composables/useRecipes';

const router = useRouter();
const { minhasReceitas, outrasReceitas, loading, error, fetchAllRecipes } = useRecipes();

// Dados para exibir: usa do Supabase
const myRecipes = computed(() => {
  return minhasReceitas.value || [];
});

const otherRecipes = computed(() => {
  return outrasReceitas.value || [];
});

const responsiveOptions = ref([
  {
    breakpoint: '1024px',
    numVisible: 3,
    numScroll: 1
  },
  {
    breakpoint: '768px',
    numVisible: 2,
    numScroll: 1
  },
  {
    breakpoint: '560px',
    numVisible: 1,
    numScroll: 1
  }
]);

// Carregar receitas ao montar o componente
onMounted(async () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  await fetchAllRecipes(user.email || null);
});

const goToRecipe = (recipeId) => {
  router.push(`/recipes/${recipeId}`);
};
</script>

<style scoped>
.recipes {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
}

.recipes-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h2 {
  color: #1ab394;
  margin: 0;
  font-size: 1.8rem;
}

.see-all {
  color: #5d5d5d;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s;
}

.see-all:hover {
  color: #5d5d5d;
  text-decoration: underline;
}

.recipe-carousel {
  width: 100%;
}

.recipe-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  margin: 0 0.5rem;
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
