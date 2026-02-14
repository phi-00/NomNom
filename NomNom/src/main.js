import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import ToastService from 'primevue/toastservice'
import App from './App.vue'
import router from './router'

createApp(App)
	.use(router)
	.use(PrimeVue, {
		theme: {
			preset: Aura
		}
	})
	.use(ToastService)
	.mount('#app')