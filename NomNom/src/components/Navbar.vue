<template>
  <nav class="navbar">
    <div class="navbar-group">
      <img src="/logo_white_bg.png" alt="Logo" class="logo" />
      <div class="navbar-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <template v-if="isAuthenticated">
          <router-link to="/recipes" class="nav-link">Recipes</router-link>
          <router-link to="/myfridge" class="nav-link">MyFridge</router-link>
          <router-link to="/shoppinglist" class="nav-link">ShoppingList</router-link>
          <router-link to="/ingredientes" class="nav-link">Ingredientes</router-link>
        </template>
      </div>
    </div>
    <div class="navbar-auth">
      <template v-if="isAuthenticated">
        <router-link to="/profile" class="user-name">👤 {{ userName }}</router-link>
        <button @click="handleLogout" class="btn-logout">Sair</button>
      </template>
      <template v-else>
        <router-link to="/login" class="btn-login">Entrar</router-link>
        <router-link to="/register" class="btn-register">Criar Conta</router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const isAuthenticated = ref(false);
const user = ref(null);

const userName = computed(() => {
  return user.value?.name || 'Usuário';
});

const checkAuth = () => {
  const token = localStorage.getItem('access_token');
  const userData = localStorage.getItem('user');
  
  isAuthenticated.value = !!token;
  if (userData) {
    try {
      user.value = JSON.parse(userData);
    } catch (e) {
      console.error('Erro ao parsear dados do usuário:', e);
    }
  }
};

const handleLogout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
  isAuthenticated.value = false;
  user.value = null;
  router.push('/');
};

onMounted(() => {
  checkAuth();
  // Atualizar estado quando storage mudar de outra aba
  window.addEventListener('storage', checkAuth);
});

// Monitorar mudanças de rota para atualizar autenticação
// Recheck auth when route changes
watch(() => route.path, () => {
  checkAuth();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;700&display=swap');

.navbar {
  background: #fff;
  border-bottom: 1px solid #eee;
  padding: 1rem 2rem;
  font-family: 'Nunito Sans', sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #000000;
  text-decoration: none;
  font-weight: 500;
  font-size: 1em;
  font-family: 'Nunito Sans';
  transition: color 0.3s;
}

.nav-link:hover {
  color: #1ab394;
}

.nav-link.router-link-exact-active {
  color: #1ab394;
  font-weight: bold;
}

.navbar-auth {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.user-name {
  color: #333;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s;
}

.user-name:hover {
  color: #1ab394;
}

.btn-logout {
  background: #ff5252;
  color: white;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-logout:hover {
  background: #e64545;
  transform: translateY(-1px);
}

.btn-login,
.btn-register {
  text-decoration: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-login {
  color: #1ab394;
  border: 2px solid #1ab394;
  background: white;
}

.btn-login:hover {
  background: #1ab394;
  color: white;
}

.btn-register {
  background: linear-gradient(135deg, #1ab394 0%, #15935f 100%);
  color: white;
  border: 2px solid transparent;
}

.btn-register:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(26, 179, 148, 0.4);
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
  }

  .navbar-links {
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link {
    font-size: 0.9rem;
  }
}
</style>
