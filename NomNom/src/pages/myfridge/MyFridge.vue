<template>
  <section class="myfridge">
    <div class="header">
      <h1>My Fridge</h1>
      <button @click="showAddDialog = true" class="add-button">
        <span class="button-icon">+</span>
        Add Ingredient
      </button>
    </div>
    
    <div class="card">
        <Tabs value="0">
            <TabList>
                <Tab v-for="tab in tabs" :key="tab.title" :value="tab.value">{{ tab.title }}</Tab>
            </TabList>
            <TabPanels>
                <TabPanel v-for="tab in tabs" :key="tab.title" :value="tab.value">
                  <div v-if="getIngredientsByGroup(tab.grupo_alimentar).length === 0" class="empty-message">
                    No ingredient in this category
                  </div>
                  <div v-else>
                    <div  class="ingredient-item header-item">
                      <div class="quantity-column">
                        <span class="column-header">Quantity</span>
                      </div>
                      <div class="ingredient-column">
                        <span class="column-header">Ingredient</span>
                      </div>
                    </div>
                    <div v-for="item in getIngredientsByGroup(tab.grupo_alimentar)" :key="item.idIngrediente" class="ingredient-item">
                      <div class="quantity-column">
                        <div class="quantity-controls">
                          <Button 
                            icon="pi pi-minus" 
                            aria-label="Decrease quantity"
                            rounded
                            size="small"
                            class="quantity-btn"
                            @click="decreaseQuantity(item)"
                            :disabled="loading"
                          />
                          <span class="ingredient-quantity">{{ item.quantidade }}</span>
                          <Button 
                            icon="pi pi-plus" 
                            aria-label="Increase quantity"
                            rounded
                            size="small"
                            class="quantity-btn"
                            @click="increaseQuantity(item)"
                            :disabled="loading"
                          />
                        </div>
                      </div>
                      <div class="ingredient-column">
                        <span class="ingredient-name">{{ item.nome }}</span>
                      </div>
                    </div>
                  </div>
                </TabPanel>
            </TabPanels>
        </Tabs>
    </div>

    <!-- Add Ingredient Dialog -->
    <div v-if="showAddDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog-content" @click.stop>
        <div class="dialog-header">
          <h2>Add Ingredient to Fridge</h2>
          <button @click="closeDialog" class="close-button">&times;</button>
        </div>

        <div class="dialog-body">
          <!-- Search for existing ingredients -->
          <div class="form-section">
            <label for="search">Search Ingredient</label>
            <input 
              id="search"
              v-model="searchQuery" 
              @input="handleSearch"
              type="text" 
              placeholder="Type to search ingredients..."
              class="search-input"
            />
            
            <!-- Search results -->
            <div v-if="searchResults.length > 0" class="search-results">
              <div 
                v-for="ingredient in searchResults" 
                :key="ingredient.id"
                @click="selectIngredient(ingredient)"
                class="search-result-item"
                :class="{ selected: selectedIngredient?.id === ingredient.id }"
              >
                <span class="result-name">{{ ingredient.nome }}</span>
                <span class="result-calories">{{ ingredient.calorias }} kcal</span>
              </div>
            </div>

            <!-- Selected ingredient display -->
            <div v-if="selectedIngredient" class="selected-ingredient">
              <div class="selected-info">
                <strong>Selected:</strong> {{ selectedIngredient.nome }}
                <span class="selected-calories">({{ selectedIngredient.calorias }} kcal)</span>
              </div>
              <button @click="clearSelection" class="clear-button">Clear</button>
            </div>
          </div>

          <!-- OR separator -->
          <div class="separator">
            <span>OR</span>
          </div>

          <!-- Create new ingredient -->
          <div class="form-section">
            <h3>Create New Ingredient</h3>
            <div class="form-group">
              <label for="newName">Name</label>
              <input 
                id="newName"
                v-model="newIngredient.nome" 
                type="text" 
                placeholder="Ingredient name"
                :disabled="!!selectedIngredient"
              />
            </div>
            <div class="form-group">
              <label for="newCalories">Calories (kcal)</label>
              <input 
                id="newCalories"
                v-model.number="newIngredient.calorias" 
                type="number" 
                placeholder="100"
                :disabled="!!selectedIngredient"
              />
            </div>
            <div class="form-group">
              <label for="newGroup">Food Group</label>
              <select 
                id="newGroup"
                v-model="newIngredient.grupo_alimentar"
                :disabled="!!selectedIngredient"
              >
                <option value="">Select a group</option>
                <option v-for="tab in tabs" :key="tab.grupo_alimentar" :value="tab.grupo_alimentar">
                  {{ tab.title }}
                </option>
              </select>
            </div>
          </div>

          <!-- Quantity input -->
          <div class="form-section">
            <div class="form-group">
              <label for="quantity">Quantity</label>
              <input 
                id="quantity"
                v-model.number="quantity" 
                type="number" 
                min="1"
                placeholder="1"
              />
            </div>
          </div>
        </div>

        <!-- Error message -->
        <div v-if="dialogError" class="error-message">
          {{ dialogError }}
        </div>

        <div class="dialog-footer">
          <button @click="closeDialog" class="cancel-button">Cancel</button>
          <button 
            @click="addIngredientToFridge" 
            class="confirm-button"
            :disabled="!canAddIngredient || addingIngredient"
          >
            {{ addingIngredient ? 'Adding...' : 'Add to Fridge' }}
          </button>
        </div>
      </div>
    </div>

  </section>
</template>

<script setup>

  import Tabs from 'primevue/tabs';
  import TabList from 'primevue/tablist';
  import Tab from 'primevue/tab';
  import TabPanels from 'primevue/tabpanels';
  import TabPanel from 'primevue/tabpanel';
  import { ref, onMounted, computed } from 'vue';
  import { useIngredients } from '../../composables/useIngredients';
  import Button from 'primevue/button';

  const { 
    ingredientes, 
    loading, 
    error, 
    fetchUserInventory,
    searchSimilarIngredients,
    createIngredient,
    addToInventory,
    updateInventoryQuantity,
    removeFromInventory
  } = useIngredients();
  
  const user = ref(null);
  const showAddDialog = ref(false);
  const searchQuery = ref('');
  const searchResults = ref([]);
  const selectedIngredient = ref(null);
  const quantity = ref(1);
  const addingIngredient = ref(false);
  const dialogError = ref(null);

  const newIngredient = ref({
    nome: '',
    calorias: null,
    grupo_alimentar: ''
  });

  onMounted(async () => {
    const userData = localStorage.getItem('user');
    if (userData) {
      user.value = JSON.parse(userData);
      await fetchUserInventory(user.value.email);
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

  // Handle search input
  const handleSearch = async () => {
    if (searchQuery.value.trim().length < 2) {
      searchResults.value = [];
      return;
    }

    const results = await searchSimilarIngredients(searchQuery.value);
    searchResults.value = results;
  };

  // Select an ingredient from search results
  const selectIngredient = (ingredient) => {
    selectedIngredient.value = ingredient;
    searchQuery.value = ingredient.nome;
    searchResults.value = [];
    // Clear new ingredient form when selecting from database
    newIngredient.value = {
      nome: '',
      calorias: null,
      grupo_alimentar: ''
    };
  };

  // Clear selection
  const clearSelection = () => {
    selectedIngredient.value = null;
    searchQuery.value = '';
    searchResults.value = [];
  };

  // Check if can add ingredient
  const canAddIngredient = computed(() => {
    if (selectedIngredient.value) {
      return quantity.value > 0;
    }
    // If creating new ingredient
    return (
      newIngredient.value.nome.trim() !== '' &&
      newIngredient.value.calorias > 0 &&
      newIngredient.value.grupo_alimentar !== '' &&
      quantity.value > 0
    );
  });

  // Add ingredient to fridge
  const addIngredientToFridge = async () => {
    if (!canAddIngredient.value || !user.value) {
      console.log('Cannot add ingredient - validation failed or no user');
      return;
    }

    addingIngredient.value = true;
    dialogError.value = null;

    try {
      let ingredientId;

      // If creating a new ingredient
      if (!selectedIngredient.value && newIngredient.value.nome) {
        console.log('Creating new ingredient:', newIngredient.value);
        const created = await createIngredient(newIngredient.value);
        console.log('Created ingredient response:', created);
        
        // Try different possible ID field names
        ingredientId = created.id || created.idIngrediente || created.ID;
        
        if (!ingredientId) {
          throw new Error('Created ingredient has no ID field. Response: ' + JSON.stringify(created));
        }
      } else if (selectedIngredient.value) {
        console.log('Using selected ingredient:', selectedIngredient.value);
        ingredientId = selectedIngredient.value.id || selectedIngredient.value.idIngrediente;
      }

      if (!ingredientId) {
        throw new Error('No ingredient ID found');
      }

      console.log('Adding to inventory - User:', user.value.email, 'Ingredient ID:', ingredientId, 'Quantity:', quantity.value);
      
      // Add to inventory
      const result = await addToInventory(user.value.email, ingredientId, quantity.value);
      console.log('Add to inventory result:', result);

      // Refresh the inventory
      await fetchUserInventory(user.value.email);

      // Close dialog and reset form
      closeDialog();
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error adding ingredient to fridge';
      dialogError.value = errorMessage;
      console.error('Error adding ingredient:', err);
      console.error('Error details:', {
        response: err.response?.data,
        message: err.message,
        status: err.response?.status
      });
    } finally {
      addingIngredient.value = false;
    }
  };

  // Close dialog and reset form
  const closeDialog = () => {
    showAddDialog.value = false;
    searchQuery.value = '';
    searchResults.value = [];
    selectedIngredient.value = null;
    quantity.value = 1;
    dialogError.value = null;
    newIngredient.value = {
      nome: '',
      calorias: null,
      grupo_alimentar: ''
    };
  };

  // Increase ingredient quantity
  const increaseQuantity = async (item) => {
    if (!user.value) return;
    
    try {
      const newQuantity = item.quantidade + 1;
      await updateInventoryQuantity(user.value.email, item.idIngrediente, newQuantity);
      await fetchUserInventory(user.value.email);
    } catch (err) {
      console.error('Erro ao aumentar quantidade:', err);
    }
  };

  // Decrease ingredient quantity or remove if reaches 0
  const decreaseQuantity = async (item) => {
    if (!user.value) return;
    
    try {
      if (item.quantidade > 1) {
        const newQuantity = item.quantidade - 1;
        await updateInventoryQuantity(user.value.email, item.idIngrediente, newQuantity);
      } else {
        // Remove ingredient if quantity reaches 0
        await removeFromInventory(user.value.email, item.idIngrediente);
      }
      await fetchUserInventory(user.value.email);
    } catch (err) {
      console.error('Erro ao diminuir quantidade:', err);
    }
  };

</script>


<style scoped>
.myfridge {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
  color: var(--text-primary);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  color: #1ab394;
  margin: 0;
}

.add-button {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(26, 179, 148, 0.3);
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(26, 179, 148, 0.4);
}

.add-button:active {
  transform: translateY(0);
}

.button-icon {
  font-size: 1.5rem;
  font-weight: bold;
}

.ingredient-item {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0.75rem 3rem;
  margin: 0.5rem 0;
  background: var(--bg-secondary);
  border-radius: 6px;
  transition: all 0.2s;
}

.ingredient-item.header-item {
  background: rgba(26, 179, 148, 0.1);
  font-weight: 700;
  border: 1px solid rgba(26, 179, 148, 0.3);
}

.ingredient-item:not(.header-item):hover {
  background: var(--card-hover);
  transform: translateX(4px);
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-controls :deep(.quantity-btn) {
  color: var(--accent-color) !important;
  width: 2rem;
  height: 2rem;
}

.quantity-controls :deep(.quantity-btn .p-button-icon) {
  color: var(--accent-color) !important;
  font-size: 1rem;
}

.quantity-controls :deep(.quantity-btn:hover) {
  background: rgba(26, 179, 148, 0.2) !important;
}

.quantity-controls :deep(.quantity-btn:hover .p-button-icon) {
  color: var(--text-primary) !important;
}

.quantity-controls :deep(.quantity-btn:disabled) {
  opacity: 0.5;
  cursor: not-allowed;
}

.ingredient-name {
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

.ingredient-quantity {
  color: var(--accent-color);
  font-weight: 700;
  min-width: 40px;
  text-align: center;
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-style: italic;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
  backdrop-filter: blur(4px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.dialog-content {
  background-color: #ffffff;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
  animation: slideUp 0.3s ease;
  position: relative;
  z-index: 1001;
  border: 2px solid rgba(26, 179, 148, 0.4);
  display: flex;
  flex-direction: column;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid rgba(26, 179, 148, 0.3);
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
}

.dialog-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.dialog-body {
  padding: 1.5rem;
}

.form-section {
  margin-bottom: 1.5rem;
}

.form-section h3 {
  color: #213547;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-weight: 600;
  font-size: 0.9rem;
}

.search-input,
.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  color: #213547;
  font-size: 1rem;
  transition: all 0.3s;
}

.search-input:focus,
.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1);
}

.form-group input:disabled,
.form-group select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.search-results {
  margin-top: 0.5rem;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.search-result-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #f0f0f0;
}

.search-result-item.selected {
  background: rgba(26, 179, 148, 0.15);
  border-left: 3px solid var(--accent-color);
}

.result-name {
  color: var(--text-primary);
  font-weight: 600;
}

.result-calories {
  color: var(--accent-color);
  font-size: 0.9rem;
}

.selected-ingredient {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(26, 179, 148, 0.1);
  border: 1px solid rgba(26, 179, 148, 0.3);
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.selected-info {
  color: var(--text-primary);
}

.selected-calories {
  color: var(--accent-color);
  margin-left: 0.5rem;
}

.clear-button {
  background: #e0e0e0;
  color: #666;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  font-weight: 600;
}

.clear-button:hover {
  background: #d0d0d0;
  color: #213547;
}

.separator {
  text-align: center;
  position: relative;
  margin: 2rem 0;
}

.separator::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: #e0e0e0;
}

.separator span {
  background: #ffffff;
  padding: 0 1rem;
  position: relative;
  color: #666;
  font-weight: 600;
}

.dialog-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
  justify-content: flex-end;
  background: #f8f9fa;
}

.cancel-button,
.confirm-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-button {
  background: #e0e0e0;
  color: #666;
}

.cancel-button:hover {
  background: #d0d0d0;
  color: #213547;
}

.confirm-button {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(26, 179, 148, 0.3);
}

.confirm-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(26, 179, 148, 0.4);
}

.confirm-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  margin: 1rem 1.5rem;
  padding: 1rem;
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  color: #f44336;
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .myfridge {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .add-button {
    width: 100%;
    justify-content: center;
  }

  .ingredient-item {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .quantity-controls {
    order: 1;
  }

  .ingredient-name {
    order: 2;
    width: 100%;
  }

  .dialog-content {
    width: 95%;
    max-height: 95vh;
  }

  .dialog-footer {
    flex-direction: column;
  }

  .cancel-button,
  .confirm-button {
    width: 100%;
  }
}
</style>
