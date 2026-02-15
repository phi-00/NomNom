import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/home/Home.vue'
import Recipes from './pages/recipes/Recipes.vue'
import RecipeDetail from './pages/recipes/RecipeDetail.vue'
import MyRecipes from './pages/recipes/MyRecipes.vue'
import OtherRecipes from './pages/recipes/OtherRecipes.vue'
import MyFridge from './pages/myfridge/MyFridge.vue'
import ShoppingList from './pages/shoppinglist/ShoppingList.vue'
import Profile from './pages/user_profile/Profile.vue'
import Login from './pages/auth/Login.vue'
import Register from './pages/auth/Register.vue'
import CompleteProfile from './pages/auth/CompleteProfile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: false } },
  { path: '/login', name: 'Login', component: Login, meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: Register, meta: { requiresAuth: false } },
  { path: '/complete-profile', name: 'CompleteProfile', component: CompleteProfile, meta: { requiresAuth: true } },
  { path: '/recipes', name: 'Recipes', component: Recipes, meta: { requiresAuth: true } },
  { path: '/recipes/:id', name: 'RecipeDetail', component: RecipeDetail, meta: { requiresAuth: true } },
  { path: '/recipes/myrecipes', name: 'MyRecipes', component: MyRecipes, meta: { requiresAuth: true } },
  { path: '/recipes/otherrecipes', name: 'OtherRecipes', component: OtherRecipes, meta: { requiresAuth: true } },
  { path: '/myfridge', name: 'MyFridge', component: MyFridge, meta: { requiresAuth: true } },
  { path: '/shoppinglist', name: 'ShoppingList', component: ShoppingList, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guard de navegação para proteger rotas
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirecionar para login se a rota requer autenticação
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    // Redirecionar para recipes se já estiver autenticado
    next('/recipes')
  } else {
    next()
  }
})

export default router
