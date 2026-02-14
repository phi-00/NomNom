<template>
  <div class="shopping-list-wrapper">
    <Toast />
    <Dialog v-model:visible="showNotFoundDialog" modal header="Items Not Found" :style="{ width: '600px' }">
      <div class="not-found-dialog">
        <p class="dialog-message">The following items were not found in the database:</p>
        
        <div v-for="(item, index) in notFoundItems" :key="index" class="not-found-item">
          <h3>"{{ item }}"</h3>
          
          <!-- Search similar -->
          <div class="search-section">
            <Button @click="searchSimilar(item, index)" label="Search Similar" icon="pi pi-search" size="small" />
            
            <div v-if="similarResults[index]?.length > 0" class="similar-results">
              <p class="similar-title">Similar items found:</p>
              <div v-for="similar in similarResults[index]" :key="similar.id" class="similar-item">
                <span>{{ similar.nome }} ({{ similar.grupo_alimentar }})</span>
                <Button @click="useExistingItem(item, similar)" label="Use This" size="small" />
              </div>
            </div>
            <div v-else-if="similarResults[index] !== undefined" class="no-results">
              No similar items found
            </div>
          </div>

          <!-- Create new -->
          <div class="create-section">
            <Button @click="showCreateForm[index] = !showCreateForm[index]" 
                    :label="showCreateForm[index] ? 'Cancel' : 'Create New Ingredient'" 
                    icon="pi pi-plus" 
                    size="small"
                    severity="success" />
            
            <div v-if="showCreateForm[index]" class="create-form">
              <InputText v-model="newIngredient[index].nome" placeholder="Name" class="form-input" />
              <Select v-model="newIngredient[index].grupo_alimentar" 
                      :options="foodGroups" 
                      placeholder="Food Group" 
                      class="form-input" />
              <InputText v-model="newIngredient[index].unidade_medida" placeholder="Unit (e.g., g, ml, un)" class="form-input" />
              <InputNumber v-model="newIngredient[index].calorias" placeholder="Calories" class="form-input" />
              <Button @click="createAndAddItem(item, index)" label="Create & Add to Fridge" severity="success" />
            </div>
          </div>

          <Divider v-if="index < notFoundItems.length - 1" />
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
    itemsNotFound.forEach((item, index) => {
      showCreateForm.value[index] = false;
      newIngredient.value[index] = {
        nome: item,
        grupo_alimentar: '',
        unidade_medida: 'g',
        calorias: 0
      };
    });
    showNotFoundDialog.value = true;
  }
}

const searchSimilar = async (itemName, index) => {
  const results = await searchSimilarIngredients(itemName);
  similarResults.value[index] = results;
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
    
    // Remove from not found list
    notFoundItems.value = notFoundItems.value.filter(item => item !== originalName);
    
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

const createAndAddItem = async (originalName, index) => {
  const ingredientData = newIngredient.value[index];
  
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
    
    // Remove from not found list
    notFoundItems.value = notFoundItems.value.filter(item => item !== originalName);
    
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
  color: #666;
  margin-bottom: 2rem;
}

/* Add item section */
.add-item-container {
  display: flex;
  gap: 0.5rem;
  width: 100%;
  margin-bottom: 2rem;
}

.item-input {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
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
  color: #999;
  padding: 2rem;
  font-style: italic;
}

.item-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.item-row:hover {
  background-color: #e9ecef;
}

.item-label {
  flex: 1;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.item-label.completed {
  text-decoration: line-through;
  color: #999;
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
}

.dialog-message {
  margin-bottom: 1.5rem;
  color: #666;
  font-size: 0.95rem;
}

.not-found-item {
  margin: 1rem 0;
}

.not-found-item h3 {
  color: #1ab394;
  margin-bottom: 1rem;
}

.search-section, .create-section {
  margin: 1rem 0;
}

.similar-results {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.similar-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.similar-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  margin: 0.5rem 0;
  background: white;
  border-radius: 4px;
}

.no-results {
  margin-top: 0.5rem;
  color: #999;
  font-style: italic;
}

.create-form {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-input {
  width: 100%;
}

/* Statistics */
.stats {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #e7f5f1;
  border-radius: 8px;
  color: #1ab394;
  font-weight: 600;
  width: 100%;
  text-align: center;
}
</style>


