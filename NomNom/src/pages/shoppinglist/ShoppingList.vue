<template>
  <div class="shopping-list-wrapper">
    <Toast />
    <Dialog v-model:visible="showNotFoundDialog" modal header="Items Not Found" :style="{ width: '600px' }">
      <div class="not-found-dialog">
        <p class="dialog-message">The following items were not found in the database:</p>
        
        <div v-for="item in notFoundItems" :key="item" class="not-found-item">
          <h3>"{{ item }}"</h3>
          
          <!-- Search similar -->
          <div class="search-section">
            <Button @click="searchSimilar(item)" label="Search Similar" icon="pi pi-search" size="small" />
            
            <div v-if="similarResults[item]?.length > 0" class="similar-results">
              <p class="similar-title">Similar items found:</p>
              <div v-for="similar in similarResults[item]" :key="similar.id" class="similar-item">
                <span>{{ similar.nome }} ({{ similar.grupo_alimentar }})</span>
                <Button @click="useExistingItem(item, similar)" label="Use This" size="small" />
              </div>
            </div>
            <div v-else-if="similarResults[item] !== undefined" class="no-results">
              No similar items found
            </div>
          </div>

          <!-- Create new -->
          <div class="create-section">
            <Button @click="toggleCreateForm(item)" 
                    :label="showCreateForm[item] ? 'Cancel' : 'Create New Ingredient'" 
                    icon="pi pi-plus" 
                    size="small"
                    severity="success" />
            
            <div v-if="showCreateForm[item]" class="create-form">
              <InputText v-model="newIngredient[item].nome" placeholder="Name" class="form-input" />
              <Select v-model="newIngredient[item].grupo_alimentar" 
                      :options="foodGroups" 
                      placeholder="Food Group" 
                      class="form-input" />
              <InputText v-model="newIngredient[item].unidade_medida" placeholder="Unit (e.g., g, ml, un)" class="form-input" />
              <InputNumber v-model="newIngredient[item].calorias" placeholder="Calories" class="form-input" />
              <Button @click="createAndAddItem(item)" label="Create & Add to Fridge" severity="success" />
            </div>
          </div>

          <Divider v-if="notFoundItems.indexOf(item) < notFoundItems.length - 1" />
        </div>
      </div>
      
      <template #footer>
        <Button label="Close" @click="showNotFoundDialog = false" severity="secondary" />
      </template>
    </Dialog>

    <section class="shoppinglist">
      <h1>Shopping List</h1>

    <div class="add-item-container">
      <InputText 
        v-model="newItemText" 
        placeholder="New item..." 
        @keyup.enter="addItem"
        class="item-input"
      />
      <button @click="addItem" class="add-button">Adicionar</button>
    </div>

    <div class="items-container">
      <div v-if="shoppingItems.length === 0" class="empty-message">
        Your shopping list is empty.
      </div>
      
      <div 
        v-for="item in shoppingItems" 
        :key="item.id" 
        class="item-row"
      >
        <Checkbox 
          v-model="item.completed" 
          :inputId="`item-${item.id}`" 
          :binary="true"
        />
        <label 
          :for="`item-${item.id}`" 
          :class="{ 'completed': item.completed }"
          class="item-label"
        >
          {{ item.text }}
        </label>
        <button @click="removeItem(item.id)" class="remove-button">
          ×
        </button>
      </div>
    </div>

    <div v-if="hasCompletedItems" class="save-container">
      <button @click="saveChanges" class="save-button">
        Add to fridge
      </button>
    </div>

  </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Checkbox from 'primevue/checkbox';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Select from 'primevue/select';
import Divider from 'primevue/divider';
import { useIngredients } from '../../composables/useIngredients';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

// Composables
const { searchIngredientByName, searchSimilarIngredients, createIngredient, addToInventory, loading } = useIngredients();
const toast = useToast();

// Reactive data
const newItemText = ref('');
const shoppingItems = ref([]);
const user = ref(null);
const showNotFoundDialog = ref(false);
const notFoundItems = ref([]);
const similarResults = ref({});
const showCreateForm = ref({});
const newIngredient = ref({});
const foodGroups = ['fruta', 'ovos', 'laticíneos', 'pescado', 'especiarias', 'cereais e derivados, tuberculos', 'hortícolas', 'carnes', 'leguminosas'];
let nextId = 1;

// Get user from localStorage on mount
onMounted(() => {
  const userData = localStorage.getItem('user');
  if (userData) {
    user.value = JSON.parse(userData);
  }
});

// Add new item to the list
const addItem = () => {
  if (newItemText.value.trim() !== '') {
    shoppingItems.value.push({
      id: nextId++,
      text: newItemText.value.trim(),
      completed: false
    });
    newItemText.value = '';
  }
};

const removeItem = (id) => {
  shoppingItems.value = shoppingItems.value.filter(item => item.id !== id);
};

const hasCompletedItems = computed(() => {
  return shoppingItems.value.some(item => item.completed);
});

const saveChanges = async () => {
  if (!user.value) {
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: 'Please log in to add items to your fridge', 
      life: 3000 
    });
    return;
  }

  const completedItems = shoppingItems.value.filter(item => item.completed);
  
  if (completedItems.length === 0) return;

  let addedCount = 0;
  let itemsNotFound = [];

  for (const item of completedItems) {
    try {
      const ingredient = await searchIngredientByName(item.text);
      
      if (ingredient) {
        await addToInventory(user.value.email, ingredient.id, 1);
        addedCount++;
      } else {
        itemsNotFound.push(item.text);
      }
    } catch (err) {
      console.error(`Error adding ${item.text}:`, err);
      itemsNotFound.push(item.text);
    }
  }

  shoppingItems.value = shoppingItems.value.filter(item => !item.completed);

  if (addedCount > 0) {
    toast.add({ 
      severity: 'success', 
      summary: 'Success', 
      detail: `${addedCount} item(s) added to your fridge!`, 
      life: 3000 
    });
  }

  if (itemsNotFound.length > 0) {
    // Initialize form data for each not found item
    notFoundItems.value = itemsNotFound;
    
    // Reset reactive objects
    similarResults.value = {};
    showCreateForm.value = {};
    newIngredient.value = {};
    
    itemsNotFound.forEach((item) => {
      showCreateForm.value[item] = false;
      newIngredient.value[item] = {
        nome: item,
        grupo_alimentar: '',
        unidade_medida: 'g',
        calorias: 0
      };
    });
    showNotFoundDialog.value = true;
  }
}

const searchSimilar = async (itemName) => {
  const results = await searchSimilarIngredients(itemName);
  // Create a new object to ensure Vue reactivity
  similarResults.value = { ...similarResults.value, [itemName]: results };
};

const toggleCreateForm = (itemName) => {
  showCreateForm.value = { ...showCreateForm.value, [itemName]: !showCreateForm.value[itemName] };
};

const useExistingItem = async (originalName, ingredient) => {
  try {
    await addToInventory(user.value.email, ingredient.id, 1);
    toast.add({ 
      severity: 'success', 
      summary: 'Success', 
      detail: `"${originalName}" added as "${ingredient.nome}" to your fridge!`, 
      life: 3000 
    });
    
    // Remove from not found list and clean up related data
    notFoundItems.value = notFoundItems.value.filter(item => item !== originalName);
    
    // Clean up the data for the removed item
    const newSimilarResults = { ...similarResults.value };
    const newShowCreateForm = { ...showCreateForm.value };
    const newIngredientData = { ...newIngredient.value };
    
    delete newSimilarResults[originalName];
    delete newShowCreateForm[originalName];
    delete newIngredientData[originalName];
    
    similarResults.value = newSimilarResults;
    showCreateForm.value = newShowCreateForm;
    newIngredient.value = newIngredientDataData;
    
    if (notFoundItems.value.length === 0) {
      showNotFoundDialog.value = false;
    }
  } catch (err) {
    console.error('Error in useExistingItem:', err);
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: err.response?.data?.detail || 'Failed to add item to fridge', 
      life: 5000 
    });
  }
};

const createAndAddItem = async (originalName) => {
  const ingredientData = newIngredient.value[originalName];
  
  if (!ingredientData.nome || !ingredientData.grupo_alimentar) {
    toast.add({ 
      severity: 'warn', 
      summary: 'Warning', 
      detail: 'Please fill in name and food group', 
      life: 3000 
    });
    return;
  }
  
  try {
    // Create the new ingredient
    const created = await createIngredient(ingredientData);
    
    // Add to inventory
    await addToInventory(user.value.email, created.id, 1);
    
    toast.add({ 
      severity: 'success', 
      summary: 'Success', 
      detail: `"${ingredientData.nome}" created and added to your fridge!`, 
      life: 3000 
    });
    
    // Remove from not found list and clean up related data
    notFoundItems.value = notFoundItems.value.filter(item => item !== originalName);
    
    // Clean up the data for the removed item
    const newSimilarResults = { ...similarResults.value };
    const newShowCreateForm = { ...showCreateForm.value };
    const newNewIngredient = { ...newIngredient.value };
    
    delete newSimilarResults[originalName];
    delete newShowCreateForm[originalName];
    delete newNewIngredient[originalName];
    
    similarResults.value = newSimilarResults;
    showCreateForm.value = newShowCreateForm;
    newIngredient.value = newNewIngredient;
    
    if (notFoundItems.value.length === 0) {
      showNotFoundDialog.value = false;
    }
  } catch (err) {
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: 'Failed to create ingredient', 
      life: 3000 
    });
  }
}

</script>

<style scoped>
.shopping-list-wrapper {
  width: 100%;
  height: 100%;
}

.shoppinglist {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  min-height: 60vh;
  font-family: 'Nunito Sans';
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  color: #1ab394;
  margin-bottom: 0.5rem;
}

p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

/* Add item section */
.add-item-container {
  display: flex;
  gap: 0.5rem;
  width: 100%;
  margin-bottom: 2rem;
  font-family: 'Nunito Sans';
}

.item-input {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-primary);
  transition: border-color 0.3s;
}

.item-input:focus {
  outline: none;
  border-color: #1ab394;
}

.add-button {
  padding: 0.75rem 1.5rem;
  background-color: #1ab394;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: 600;
}

.add-button:hover {
  background-color: #148f7a;
}

/* Items container */
.items-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty-message {
  text-align: center;
  color: var(--text-secondary);
  padding: 2rem;
  font-style: italic;
}

.item-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background-color: var(--bg-card);
  border: 1px solid rgba(26, 179, 148, 0.2);
  border-radius: 8px;
  transition: all 0.3s;
}

.item-row:hover {
  background-color: var(--card-hover);
  border-color: rgba(26, 179, 148, 0.4);
}

.item-label {
  flex: 1;
  cursor: pointer;
  font-size: 1rem;
  color: var(--text-primary);
  font-family: 'Nunito Sans', sans-serif;
  transition: all 0.3s;
}

.item-label.completed {
  text-decoration: line-through;
  color: var(--text-secondary);
  opacity: 0.6;
}

.remove-button {
  padding: 0.25rem 0.5rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.3s;
  line-height: 1;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.save-button {
  padding: 0.75rem 1.5rem;
  background-color: #1ab394;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: 600;
}

.remove-button:hover {
  background-color: #c82333;
}

.save-button:hover {
  background-color: #148f7a;
}

.save-container {
  width: 100%;
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

/* Not Found Dialog Styles */
.not-found-dialog {
  padding: 1rem 0;
  font-family: 'Nunito Sans';
}

:deep(.p-dialog) {
  background-color: var(--bg-card) !important;
  border: 1px solid rgba(26, 179, 148, 0.3) !important;
}

:deep(.p-dialog-header) {
  background-color: var(--bg-card) !important;
  border-bottom: 2px solid rgba(26, 179, 148, 0.3) !important;
  padding: 1.5rem !important;
  font-family: 'Nunito Sans', sans-serif !important;
}

:deep(.p-dialog-header-title) {
  color: var(--text-primary) !important;
  font-family: 'Nunito Sans';
  font-weight: 600 !important;
}

:deep(.p-dialog-header-close) {
  color: var(--text-primary) !important;
  font-family: 'Nunito Sans';
}

:deep(.p-dialog-content) {
  background-color: var(--bg-card) !important;
  color: var(--text-primary) !important;
  font-family: 'Nunito Sans';
}

:deep(.p-dialog-footer) {
  background-color: var(--bg-card) !important;
  border-top: 2px solid rgba(26, 179, 148, 0.3) !important;
  padding: 1.5rem !important;
  font-family: 'Nunito Sans';
}

.dialog-message {
  margin-bottom: 1.5rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-family: 'Nunito Sans';
}

.not-found-item {
  margin: 1rem 0;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border-left: 4px solid #1ab394;
  font-family: 'Nunito Sans';
}

.not-found-item h3 {
  color: #1ab394;
  margin-bottom: 1rem;
  font-family: 'Nunito Sans';
}

.search-section, .create-section {
  margin: 1rem 0;
}

.similar-results {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid rgba(26, 179, 148, 0.2);
}

.similar-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1ab394;
  font-family: 'Nunito Sans', sans-serif;
}

.similar-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  margin: 0.5rem 0;
  background: var(--bg-card);
  border-radius: 4px;
  color: var(--text-primary);
  font-family: 'Nunito Sans', sans-serif;
}

.no-results {
  margin-top: 0.5rem;
  color: var(--text-secondary);
  font-style: italic;
  font-family: 'Nunito Sans', sans-serif;
}

.create-form {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid rgba(26, 179, 148, 0.2);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-input {
  width: 100%;
  font-family: 'Nunito Sans', sans-serif;
}

/* Statistics */
.stats {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: rgba(26, 179, 148, 0.15);
  border-radius: 8px;
  color: #1ab394;
  font-weight: 600;
  width: 100%;
  text-align: center;
}
</style>


