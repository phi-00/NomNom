<template>
  <section class="myfridge">
    <h1>MyFridge</h1>
    
    <div class="card">
        <Tabs value="0">
            <TabList>
                <Tab v-for="tab in tabs" :key="tab.title" :value="tab.value">{{ tab.title }}</Tab>
            </TabList>
            <TabPanels>
                <TabPanel v-for="tab in tabs" :key="tab.title" :value="tab.value">
                  <div v-if="getIngredientsByGroup(tab.grupo_alimentar).length === 0" class="empty-message">
                    Nenhum ingrediente nesta categoria
                  </div>
                  <div v-else>
                    <div  class="ingredient-item">
                      <span class="ingredient-quantity">Quantity</span>
                      <span class="ingredient-quantity">Ingredient</span>
                    </div>
                    <div v-for="item in getIngredientsByGroup(tab.grupo_alimentar)" :key="item.idIngrediente" class="ingredient-item">
                      <span class="ingredient-quantity">{{ item.quantidade }}</span>
                      <span class="ingredient-name">{{ item.nome }}</span>
                    </div>
                  </div>
                </TabPanel>
            </TabPanels>
        </Tabs>
    </div>

  </section>
</template>

<script setup>

  import Tabs from 'primevue/tabs';
  import TabList from 'primevue/tablist';
  import Tab from 'primevue/tab';
  import TabPanels from 'primevue/tabpanels';
  import TabPanel from 'primevue/tabpanel';
  import { ref, onMounted } from 'vue';
  import { useIngredients } from '../../composables/useIngredients';

  const { ingredientes, loading, error, fetchUserInventory } = useIngredients();
  const user = ref(null);

  onMounted(async () => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);
      await fetchUserInventory(user.email);
    }
  });

  // Filter ingredients by food group
  const getIngredientsByGroup = (grupo) => {
    if (!ingredientes.value) return [];
    return ingredientes.value.filter(item => item.grupo_alimentar === grupo);
  };

  const tabs = ref([
    { title: 'Fruit', grupo_alimentar: 'fruta', value: '0' },
    { title: 'Eggs', grupo_alimentar: 'ovos', value: '1' },
    { title: 'Dairy', grupo_alimentar: 'laticíneos', value: '2' },
    { title: 'Fish', grupo_alimentar: 'pescado', value: '3' },
    { title: 'Spices', grupo_alimentar: 'especiarias', value: '4' },
    { title: 'Cereals', grupo_alimentar: 'cereais e derivados, tuberculos', value: '5' },
    { title: 'Vegetables', grupo_alimentar: 'hortícolas', value: '6' },
    { title: 'Meat', grupo_alimentar: 'carnes', value: '7' },
    { title: 'Legumes', grupo_alimentar: 'leguminosas', value: '8' }
  ]);


</script>


<style scoped>
.myfridge {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
  color: var(--text-primary);
}
h1 {
  color: var(--accent-color);
}

.ingredient-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  background: var(--bg-secondary);
  border-radius: 8px;
  transition: all 0.2s;
}

.ingredient-item:hover {
  background: var(--card-hover);
  transform: translateX(4px);
}

.ingredient-name {
  font-weight: 600;
  color: var(--text-primary);
}

.ingredient-quantity {
  color: var(--accent-color);
  font-weight: 700;
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-style: italic;
}
</style>
