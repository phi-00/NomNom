<template>
  <section class="home">
    <!-- Hero Section -->
    <div class="hero">
      <div class="hero-content">
        <h1>Welcome to <img src="/name_white_bg.png" alt="NomNom" class="brand-name" /></h1>
        <p class="subtitle">Discover delicious recipes with the ingredients you have!</p>
        <div class="cta-buttons">
          <router-link to="/recipes" class="btn btn-primary">
            🔍 Explore Recipes
          </router-link>
          <router-link to="/myfridge" class="btn btn-secondary">
            🧊 My Fridge
          </router-link>
        </div>
      </div>
      <div class="hero-image">
        <div class="logo-animated">
          <img src="/logo_white_bg.png" alt="NomNom Logo" class="logo" />
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <h2>Why use <img src="/name_white.png" alt="NomNom" class="brand-name"/>?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🥘</div>
          <h3>Diverse Recipes</h3>
          <p>Access thousands of delicious recipes for all tastes</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🧊</div>
          <h3>Manage Your Fridge</h3>
          <p>Control the ingredients you have and get personalized suggestions</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📋</div>
          <h3>Shopping List</h3>
          <p>Create automatic shopping lists based on the recipes you choose</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">❤️</div>
          <h3>Favorites</h3>
          <p>Save your favorite recipes for quick access</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔥</div>
          <h3>Nutritional Info</h3>
          <p>Check calories and information for each recipe</p>
        </div>
      </div>
    </div>

  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Check if user is logged in
const isLoggedIn = computed(() => {
  return localStorage.getItem('user') !== null;
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700&display=swap');

.home {
  font-family: 'Nunito Sans', sans-serif;
  color: var(--text-primary);
  background: var(--navbar-bg);
  min-height: 100vh;
  overflow-x: hidden;
}

/* Hero Section */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  padding: 4rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: 70vh;
}

.hero-content h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #ffffff;
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-content h1 .brand-name {
  max-width: 200px;
  height: auto;
  display: inline-block;
}

.subtitle {
  font-size: 1.3rem;
  color: #b0b0b0;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(26, 179, 148, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(26, 179, 148, 0.4);
}

.btn-secondary {
  background: #252525;
  color: #ffffff;
  border: 2px solid rgba(26, 179, 148, 0.4);
}

.btn-secondary:hover {
  background: #1a1a1a;
  border-color: #1ab394;
}

.hero-image {
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1000px;
}

.logo-animated {
  width: 300px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Features Section */
.features-section {
  padding: 4rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: linear-gradient(180deg, transparent 0%, rgba(26, 179, 148, 0.05) 100%);
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  color: #1ab394;
  margin-bottom: 3rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.features-section h2 .brand-name {
  max-width: 120px;
  height: auto;
  display: inline-block;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.features-grid > :nth-child(4),
.features-grid > :nth-child(5) {
  grid-column: span 1;
}

@media (min-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .features-grid > :nth-child(1),
  .features-grid > :nth-child(2),
  .features-grid > :nth-child(3) {
    grid-column: span 2;
  }
  
  .features-grid > :nth-child(4) {
    grid-column: 2 / span 2;
  }
  
  .features-grid > :nth-child(5) {
    grid-column: 4 / span 2;
  }
}

.feature-card {
  background: #1a1a1a;
  border: 2px solid rgba(26, 179, 148, 0.2);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: #1ab394;
  box-shadow: 0 8px 25px rgba(26, 179, 148, 0.15);
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.feature-card h3 {
  color: #ffffff;
  font-size: 1.3rem;
  margin: 1rem 0 0.5rem 0;
}

.feature-card p {
  color: #b0b0b0;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* Stats Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.stat-card {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  padding: 2.5rem;
  border-radius: 12px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 15px rgba(26, 179, 148, 0.3);
}

.stat-number {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-label {
  display: block;
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 500;
}

/* Get Started Section */
.get-started-section {
  padding: 4rem 2rem;
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
}

.get-started-section h2 {
  font-size: 2.5rem;
  color: #1ab394;
  margin-bottom: 1rem;
  font-weight: 700;
}

.get-started-section p {
  font-size: 1.2rem;
  color: #b0b0b0;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.explore-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 2rem;
    min-height: auto;
  }

  .logo {
    width: 200px;
    height: 200px;
  }

  .hero-content h1 {
    font-size: 2.5rem;
  }

  .subtitle {
    font-size: 1.1rem;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 2rem 1rem;
  }

  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-content h1 .brand-name {
    max-width: 150px;
  }

  .subtitle {
    font-size: 1rem;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .features-section h2,
  .get-started-section h2 {
    font-size: 1.8rem;
  }

  .features-section h2 .brand-name {
    max-width: 80px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .logo-animated {
    width: 150px;
    height: 150px;
  }

  .stat-card {
    padding: 1.5rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .explore-buttons {
    flex-direction: column;
  }

  .explore-buttons .btn {
    width: 100%;
  }
}
</style>
