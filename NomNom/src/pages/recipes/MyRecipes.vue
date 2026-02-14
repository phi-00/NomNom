<template>
  <section class="my-recipes">
    <h1>My Recipes</h1>
    <div class="recipes-grid">
      <div class="recipe-card" v-for="recipe in myRecipes" :key="recipe.id">
        <img :src="recipe.image" :alt="recipe.name" />
        <h3>{{ recipe.name }}</h3>
        <p>{{ recipe.description }}</p>
        <span class="time">⏱️ {{ recipe.time }}</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const myRecipes = ref([
  {
    id: 1,
    name: 'Spaghetti Carbonara',
    description: 'Classic Italian pasta dish',
    time: '30 min',
    image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400'
  },
  {
    id: 2,
    name: 'Caesar Salad',
    description: 'Fresh and crispy salad',
    time: '15 min',
    image: 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400'
  },
  {
    id: 3,
    name: 'Grilled Salmon',
    description: 'Healthy and delicious',
    time: '25 min',
    image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400'
  }
]);
</script>

<style scoped>
.my-recipes {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
}

h1 {
  color: #1ab394;
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.recipe-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
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

.recipe-card .time {
  display: inline-block;
  margin-top: 0.5rem;
  color: #1ab394;
  font-weight: 500;
}
</style>
