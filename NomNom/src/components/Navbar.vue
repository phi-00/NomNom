<template>
  <nav class="navbar">
    <div class="navbar-group">
      <img src="/vite.svg" alt="Logo" class="logo" />
      <div class="navbar-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/recipes" class="nav-link">Recipes</router-link>
        <router-link to="/myfridge" class="nav-link">MyFridge</router-link>
        <router-link to="/shoppinglist" class="nav-link">ShoppingList</router-link>
        <router-link to="/ingredientes" class="nav-link">Ingredientes</router-link>
        <router-link to="/profile" class="nav-link">Profile</router-link> 
      </div>
    </div>
  </nav>
</template>

<script setup>
// Navbar não precisa de lógica por enquanto
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;700&display=swap');

.navbar {
  background: #fff;
  border-bottom: 1px solid #eee;
  padding: 1rem 2rem;
  font-family: 'Nunito Sans', sans-serif;
}
.navbar-group {
  display: flex;
  align-items: center;
}
.logo {
  height: 40px;
  margin-right: 3rem;
}
.navbar-links {
  display: flex;
  gap: 4rem;
}
.nav-link {
  color: #000000;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1em;
  font-family: 'Nunito Sans';
}
.nav-link.router-link-exact-active {
  color: #1ab394;
  font-weight: bold;
}
</style>
