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

// Dados default em caso de não haver dados no Supabase
const defaultMyRecipes = ref([
  {
    id: 1,
    name: 'Spaghetti Carbonara',
    description: 'Classic Italian pasta dish',
    time: '30 min',
    tags: ['Vegetariana'],
    image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400'
  },
  {
    id: 2,
    name: 'Caesar Salad',
    description: 'Fresh and crispy salad',
    time: '15 min',
    tags: ['Vegan', 'Vegetariana'],
    image: 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400'
  },
  {
    id: 3,
    name: 'Grilled Salmon',
    description: 'Healthy and delicious',
    time: '25 min',
    tags: ['Sem Glúten', 'Paleo'],
    image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400'
  },
  {
    id: 7,
    name: 'Pasta Primavera',
    description: 'Light and colorful vegetables',
    time: '20 min',
    tags: ['Vegan', 'Vegetariana'],
    image: 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400'
  },
  {
    id: 8,
    name: 'Beef Steak',
    description: 'Juicy and tender meat',
    time: '35 min',
    tags: ['Paleo', 'Sem Glúten'],
    image: 'https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400'
  },
  {
    id: 9,
    name: 'Mushroom Risotto',
    description: 'Creamy and savory rice dish',
    time: '40 min',
    tags: ['Vegetariana'],
    image: 'https://images.unsplash.com/photo-1476124369162-2f4ee5ddc096?w=400'
  }
]);

const defaultOtherRecipes = ref([
  {
    id: 4,
    name: 'Chocolate Cake',
    description: 'Rich and moist dessert',
    time: '45 min',
    tags: ['Vegetariana'],
    image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400'
  },
  {
    id: 5,
    name: 'Chicken Curry',
    description: 'Spicy and flavorful',
    time: '40 min',
    tags: ['Paleo', 'Sem Glúten'],
    image: 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400'
  },
  {
    id: 6,
    name: 'Vegetable Stir Fry',
    description: 'Quick and healthy',
    time: '20 min',
    tags: ['Vegan', 'Vegetariana'],
    image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400'
  },
  {
    id: 10,
    name: 'Tacos Al Pastor',
    description: 'Traditional Mexican flavors',
    time: '25 min',
    tags: ['Paleo'],
    image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400'
  },
  {
    id: 11,
    name: 'Pad Thai',
    description: 'Thai noodle stir fry',
    time: '30 min',
    tags: ['Vegan'],
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400'
  },
  {
    id: 12,
    name: 'Tiramisu',
    description: 'Classic Italian dessert',
    time: '20 min',
    tags: ['Vegetariana'],
    image: 'https://images.unsplash.com/photo-1571877227200-a0fb08a01a09?w=400'
  }
]);

// Dados para exibir: usa do Supabase ou defaults
const myRecipes = computed(() => {
  return minhasReceitas.value && minhasReceitas.value.length > 0 
    ? minhasReceitas.value 
    : defaultMyRecipes.value;
});

const otherRecipes = computed(() => {
  return outrasReceitas.value && outrasReceitas.value.length > 0 
    ? outrasReceitas.value 
    : defaultOtherRecipes.value;
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
  await fetchAllRecipes();
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
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  margin: 0 0.5rem;
  background: white;
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
  color: #333;
  margin: 0.5rem 0;
  font-size: 1.2rem;
}

.recipe-card p {
  color: #666;
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
  color: #1ab394;
  font-weight: 500;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  display: inline-block;
  background-color: #e0f5f0;
  color: #1ab394;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 0.75rem;
  font-weight: 500;
}
</style>
