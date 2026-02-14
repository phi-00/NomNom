<template>
  <section class="other-recipes">
    <h1>Other Recipes</h1>
    <div class="recipes-grid">
      <div class="recipe-card" v-for="recipe in otherRecipes" :key="recipe.id">
        <img :src="recipe.image" :alt="recipe.name" />
        <h3>{{ recipe.name }}</h3>
        <p>{{ recipe.description }}</p>
        <div class="recipe-meta">
          <span class="time">⏱️ {{ recipe.time }}</span>
          <div class="tags" v-if="recipe.tags">
            <span class="tag" v-for="tag in recipe.tags" :key="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const otherRecipes = ref([
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
  }
]);
</script>

<style scoped>
.other-recipes {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
  color: var(--text-primary);
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
