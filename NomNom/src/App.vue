<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'

const route = useRoute()
const router = useRouter()
const transitionName = ref('slide-right')

const pageOrder = ['/', '/recipes', '/myfridge', '/shoppinglist', '/ingredientes']
let prevIndex = pageOrder.indexOf(route.path)

watch(
  () => route.path,
  (to, from) => {
    const toIndex = pageOrder.indexOf(to)
    const fromIndex = prevIndex
    transitionName.value = toIndex > fromIndex ? 'slide-right' : 'slide-left'
    prevIndex = toIndex
  }
)

</script>

<template>
  <div class="app-container">
    <Navbar />
    <router-view v-slot="{ Component }">
      <transition :name="transitionName" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style scoped>
.app-container {
  background-color: var(--bg-primary);
  min-height: 100vh;
  width: 100%;
  font-family: 'Nunito Sans', sans-serif;
}

.slide-right-enter-active, .slide-right-leave-active {
  transition: transform 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}
.slide-right-enter-from {
  transform: translateX(100%);
}
.slide-right-enter-to {
  transform: translateX(0);
}
.slide-right-leave-from {
  transform: translateX(0);
}
.slide-right-leave-to {
  transform: translateX(-100%);
}

.slide-left-enter-active, .slide-left-leave-active {
  transition: transform 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}
.slide-left-enter-from {
  transform: translateX(-100%);
}
.slide-left-enter-to {
  transform: translateX(0);
}
.slide-left-leave-from {
  transform: translateX(0);
}
.slide-left-leave-to {
  transform: translateX(100%);
}
</style>

<style>
/* Global font for PrimeVue components */
.p-toast,
.p-toast .p-toast-message,
.p-toast-summary,
.p-toast-detail,
.p-dialog,
.p-button,
.p-inputtext,
.p-dropdown,
.p-component {
  font-family: 'Nunito Sans', sans-serif !important;
}
</style>
