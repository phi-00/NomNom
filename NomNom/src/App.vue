<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'

const route = useRoute()
const router = useRouter()
const transitionName = ref('slide-right')

const pageOrder = ['/', '/recipes', '/myfridge', '/shoppinglist']
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
  <Navbar />
  <transition :name="transitionName" mode="out-in">
    <router-view />
  </transition>
</template>

<style scoped>
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
