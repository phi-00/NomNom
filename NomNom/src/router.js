import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/home/Home.vue'
import Recipes from './pages/recipes/Recipes.vue'
import MyFridge from './pages/myfridge/MyFridge.vue'
import ShoppingList from './pages/shoppinglist/ShoppingList.vue'
import Profile from './pages/user_profile/Profile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/recipes', name: 'Recipes', component: Recipes },
  { path: '/myfridge', name: 'MyFridge', component: MyFridge },
  { path: '/shoppinglist', name: 'ShoppingList', component: ShoppingList },
  { path: '/profile', name: 'Profile', component: Profile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
