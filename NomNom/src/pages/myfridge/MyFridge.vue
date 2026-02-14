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
                    <div v-for="item in getIngredientsByGroup(tab.grupo_alimentar)" :key="item.idIngrediente" class="ingredient-item">
                      <span class="ingredient-name">{{ item.nome }}</span>
                      <span class="ingredient-quantity">{{ item.quantidade }}{{ item.unidade_medida }}</span>
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
    { title: 'Fruit', grupo_alimentar: 'frutas', value: '0' },
    { title: 'Eggs', grupo_alimentar: 'ovos', value: '1' },
    { title: 'Dairy', grupo_alimentar: 'lacticínios', value: '2' },
    { title: 'Fish', grupo_alimentar: 'pescado', value: '3' },
    { title: 'Spices', grupo_alimentar: 'especiarias', value: '4' },
    { title: 'Cereals', grupo_alimentar: 'cereais e derivados', value: '5' },
    { title: 'Vegetables', grupo_alimentar: 'hortícolas', value: '6' }
  ]);


</script>


<style scoped>
.myfridge {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
}
h1 {
  color: #1ab394;
}

.ingredient-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.2s;
}

.ingredient-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.ingredient-name {
  font-weight: 600;
  color: #333;
}

.ingredient-quantity {
  color: #667eea;
  font-weight: 700;
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: #999;
  font-style: italic;
}
</style>
