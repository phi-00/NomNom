<template>
  <section class="recipes">
    <h1>Recipes</h1>
    <p>Veja as receitas disponíveis.</p>
    
    <Carousel 
      :value="recipes" 
      :numVisible="3" 
      :numScroll="1" 
      :responsiveOptions="responsiveOptions"
      class="recipe-carousel"
    >
      <template #item="slotProps">
        <div class="recipe-card">
          <img :src="slotProps.data.image" :alt="slotProps.data.name" />
          <h3>{{ slotProps.data.name }}</h3>
          <p>{{ slotProps.data.description }}</p>
          <span class="time">⏱️ {{ slotProps.data.time }}</span>
        </div>
      </template>
    </Carousel>
  </section>
  
</template>

<script setup>
import Carousel from 'primevue/carousel';
import { ref } from 'vue';

const recipes = ref([
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
  },
  {
    id: 4,
    name: 'Chocolate Cake',
    description: 'Rich and moist dessert',
    time: '45 min',
    image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400'
  },
  {
    id: 5,
    name: 'Chicken Curry',
    description: 'Spicy and flavorful',
    time: '40 min',
    image: 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400'
  }
]);

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
</script>

<style scoped>
.recipes {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 2rem;
}

h1 {
  color: #42b883;
  margin-bottom: 0.5rem;
}

.recipe-carousel {
  width: 100%;
  max-width: 1200px;
  margin-top: 2rem;
}

.recipe-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  margin: 0 0.5rem;
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
  color: #42b883;
  font-weight: 500;
}
</style>
