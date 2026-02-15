<template>
  <div class="shopping-list-wrapper">
    <Toast />
    
    <section class="shoppinglist">
      <h1>Shopping List</h1>

      <!-- Search and Add Section -->
      <div class="search-section">
        <div class="search-container">
          <InputText 
            v-model="searchText" 
            placeholder="Type ingredient name..." 
            @keyup.enter="searchSimilar"
            class="search-input"
          />
          <InputNumber 
            v-model="quantidadeSelected" 
            :min="1" 
            placeholder="Qty"
            class="quantity-input"
            mode="decimal"
            :use-grouping="false"
          />
          <Button @click="searchSimilar" label="Search" icon="pi pi-search" />
        </div>

        <!-- Similar Results -->
        <div v-if="similarResults.length > 0" class="similar-results">
          <h3>Similar ingredients:</h3>
          <div v-for="ingredient in similarResults" :key="ingredient.id" class="similar-item">
            <span>{{ ingredient.nome }} ({{ ingredient.grupo_alimentar }})</span>
            <Button 
              @click="addToList(ingredient)" 
              label="Add" 
              icon="pi pi-plus"
              size="small"
              severity="success"
            />
          </div>
        </div>

        <div v-if="searchPerformed && similarResults.length === 0" class="no-results">
          <span>No similar ingredients found.</span>
          <Button 
            @click="showCreateDialog = true" 
            label="Create new" 
            icon="pi pi-plus"
            size="small"
            class="create-btn"
          />
        </div>
      </div>

      <!-- Dialog para criar novo ingrediente -->
      <Dialog 
        v-model:visible="showCreateDialog" 
        modal 
        header="Create new ingredient"
        :style="{ width: '500px' }"
      >
        <div class="create-form-dialog">
          <div class="form-group">
            <label>Ingredient name: *</label>
            <InputText 
              v-model="newIngredientForm.nome"
              placeholder="Ex: Banana"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Food group: *</label>
            <Dropdown 
              v-model="newIngredientForm.grupo_alimentar"
              :options="foodGroups"
              placeholder="Select a group"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Unit of measurement:</label>
            <InputText 
              v-model="newIngredientForm.unidade_medida"
              placeholder="Ex: g, ml, un"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Calories (per 100g):</label>
            <InputNumber 
              v-model="newIngredientForm.calorias"
              :min="0"
              class="form-input"
            />
          </div>
        </div>

        <template #footer>
          <Button 
            label="Cancel" 
            @click="showCreateDialog = false" 
            severity="secondary" 
          />
          <Button 
            label="Create and add" 
            @click="createAndAddIngredient" 
            severity="success"
          />
        </template>
      </Dialog>

      <!-- Shopping List Items -->
      <div class="items-container">
        <h2>My Shopping List</h2>
        
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
            {{ item.text }} ({{ item.quantidade }})
          </label>
          <button @click="removeItem(item.id)" class="remove-button">
            ×
          </button>
        </div>
      </div>

      <!-- Save Changes -->
      <div v-if="hasCompletedItems" class="save-container">
        <button @click="saveChanges" class="save-button">
          Add to Fridge
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
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import { useIngredients } from '../../composables/useIngredients';
import { useShoppingList } from '../../composables/useShoppingList';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

// Composables
const { searchSimilarIngredients, addToInventory, createIngredient } = useIngredients();
const { fetchShoppingList, addToShoppingList, removeFromShoppingList, shoppingListItems } = useShoppingList();
const toast = useToast();

// Food groups
const foodGroups = ['fruta', 'ovos', 'laticíneos', 'pescado', 'especiarias', 'cereais e derivados, tuberculos', 'hortícolas', 'carnes', 'leguminosas'];

// Reactive data
const searchText = ref('');
const quantidadeSelected = ref(1);
const similarResults = ref([]);
const shoppingItems = ref([]);
const user = ref(null);
const searchPerformed = ref(false);
const showCreateDialog = ref(false);
const newIngredientForm = ref({
  nome: '',
  grupo_alimentar: '',
  unidade_medida: 'g',
  calorias: 0
});

// Carrega usuário e lista de compras ao montar
onMounted(async () => {
  const userData = localStorage.getItem('user');
  if (userData) {
    user.value = JSON.parse(userData);
    await loadShoppingList();
  }
});

// Carrega lista de compras do banco
const loadShoppingList = async () => {
  try {
    await fetchShoppingList(user.value.email);
    shoppingItems.value = shoppingListItems.value.map(item => ({
      id: item.idIngrediente,
      text: item.ingrediente.nome,
      completed: false,
      quantidade: item.quantidade,
      ingredienteId: item.idIngrediente
    }));
  } catch (err) {
    console.error('Erro ao carregar lista de compras:', err);
  }
};

// Procura ingredientes semelhantes
const searchSimilar = async () => {
  if (searchText.value.trim() === '') return;
  
  try {
    searchPerformed.value = true;
    const results = await searchSimilarIngredients(searchText.value.trim());
    similarResults.value = results || [];
  } catch (err) {
    console.error('Erro ao procurar ingredientes:', err);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Error searching for ingredients',
      life: 3000
    });
  }
};

// Adiciona ingrediente à lista de compras
const addToList = async (ingredient) => {
  try {
    // Verifica se já existe na lista
    const exists = shoppingItems.value.find(item => item.id === ingredient.id);
    
    if (exists) {
      toast.add({
        severity: 'info',
        summary: 'Already exists',
        detail: 'This ingredient is already in your list',
        life: 2000
      });
      return;
    }

    const quantidade = quantidadeSelected.value || 1;

    // Adiciona ao banco de dados
    await addToShoppingList(user.value.email, ingredient.id, quantidade);
    
    // Adiciona localmente
    shoppingItems.value.push({
      id: ingredient.id,
      text: ingredient.nome,
      completed: false,
      quantidade: quantidade,
      ingredienteId: ingredient.id
    });

    // Limpa busca e reseta quantidade
    searchText.value = '';
    quantidadeSelected.value = 1;
    similarResults.value = [];
    searchPerformed.value = false;

    toast.add({
      severity: 'success',
      summary: 'Added',
      detail: `${ingredient.nome} added to list (${quantidade} un)`,
      life: 2000
    });
  } catch (err) {
    console.error('Erro ao adicionar:', err);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Error adding ingredient',
      life: 3000
    });
  }
};

// Criar novo ingrediente e adicionar à lista
const createAndAddIngredient = async () => {
  try {
    // Validar campos obrigatórios
    if (!newIngredientForm.value.nome || !newIngredientForm.value.grupo_alimentar) {
      toast.add({
        severity: 'warn',
        summary: 'Warning',
        detail: 'Please fill in the ingredient name and food group',
        life: 3000
      });
      return;
    }

    // Criar ingrediente
    const created = await createIngredient(newIngredientForm.value);

    const quantidade = quantidadeSelected.value || 1;

    // Adicionar à lista de compras no banco
    await addToShoppingList(user.value.email, created.id, quantidade);

    // Adicionar localmente
    shoppingItems.value.push({
      id: created.id,
      text: created.nome,
      completed: false,
      quantidade: quantidade,
      ingredienteId: created.id
    });

    // Limpar e resetar
    searchText.value = '';
    quantidadeSelected.value = 1;
    similarResults.value = [];
    searchPerformed.value = false;
    showCreateDialog.value = false;
    newIngredientForm.value = {
      nome: '',
      grupo_alimentar: '',
      unidade_medida: 'g',
      calorias: 0
    };

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: `"${created.nome}" created and added to list (${quantidade} un)`,
      life: 3000
    });
  } catch (err) {
    console.error('Erro ao criar ingrediente:', err);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Error creating ingredient',
      life: 3000
    });
  }
};

// Remove item da lista
const removeItem = async (id) => {
  try {
    await removeFromShoppingList(user.value.email, id);
    shoppingItems.value = shoppingItems.value.filter(item => item.id !== id);
    
    toast.add({
      severity: 'success',
      summary: 'Removed',
      detail: 'Item removed from list',
      life: 2000
    });
  } catch (err) {
    console.error('Erro ao remover:', err);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Error removing item',
      life: 3000
    });
  }
};

const hasCompletedItems = computed(() => {
  return shoppingItems.value.some(item => item.completed);
});

// Salva itens comprados (adiciona ao frigorífico e remove da lista)
const saveChanges = async () => {
  if (!user.value) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Please log in',
      life: 3000
    });
    return;
  }

  const completedItems = shoppingItems.value.filter(item => item.completed);
  if (completedItems.length === 0) return;

  let addedCount = 0;

  for (const item of completedItems) {
    try {
      await addToInventory(user.value.email, item.ingredienteId, item.quantidade || 1);
      await removeFromShoppingList(user.value.email, item.ingredienteId);
      addedCount++;
    } catch (err) {
      console.error(`Erro ao processar ${item.text}:`, err);
    }
  }

  shoppingItems.value = shoppingItems.value.filter(item => !item.completed);

  if (addedCount > 0) {
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: `${addedCount} item(s) added to fridge!`,
      life: 3000
    });
  }
};
</script>

<style scoped>
.shopping-list-wrapper {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-primary);
}

.shoppinglist {
  display: flex;
  flex-direction: column;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Nunito Sans';
}

h1 {
  color: #1ab394;
  margin-bottom: 2rem;
  font-size: 2.5rem;
}

h2 {
  color: #1ab394;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

h3 {
  color: #1ab394;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

/* Search Section */
.search-section {
  background-color: var(--bg-card);
  border: 1px solid rgba(26, 179, 148, 0.2);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.search-container {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid rgba(26, 179, 148, 0.3);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-primary);
  font-family: 'Nunito Sans';
}

.search-input:focus {
  outline: none;
  border-color: #1ab394;
}

.quantity-input {
  min-width: 90px !important;
  width: fit-content !important;
}

:deep(.quantity-input .p-inputnumber-input) {
  padding: 0.75rem !important;
  font-size: 1rem !important;
  border: 2px solid rgba(26, 179, 148, 0.3) !important;
  border-radius: 8px !important;
  background-color: var(--input-bg) !important;
  color: var(--text-primary) !important;
  font-family: 'Nunito Sans' !important;
  width: 80px !important;
}

:deep(.quantity-input .p-inputnumber-input:focus) {
  outline: none !important;
  border-color: #1ab394 !important;
}

:deep(.quantity-input .p-inputnumber-button) {
  width: 24px !important;
  padding: 0 !important;
}

/* Similar Results */
.similar-results {
  background-color: rgba(26, 179, 148, 0.1);
  border: 1px solid rgba(26, 179, 148, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.similar-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background-color: var(--bg-card);
  border-radius: 6px;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.no-results {
  text-align: center;
  color: var(--text-secondary);
  padding: 1.5rem;
  font-style: italic;
  background-color: rgba(26, 179, 148, 0.05);
  border: 1px dashed rgba(26, 179, 148, 0.2);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

:deep(.create-btn) {
  margin-top: 0.5rem !important;
}

:deep(.create-btn .p-button) {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%) !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(26, 179, 148, 0.3) !important;
}

:deep(.create-btn .p-button:hover) {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(26, 179, 148, 0.4) !important;
}

/* Items Container */
.items-container {
  background-color: var(--bg-card);
  border: 1px solid rgba(26, 179, 148, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
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
  gap: 1rem;
  padding: 1rem;
  background-color: rgba(26, 179, 148, 0.05);
  border: 1px solid rgba(26, 179, 148, 0.1);
  border-radius: 8px;
  margin-bottom: 0.75rem;
  transition: all 0.3s;
}

.item-row:hover {
  background-color: rgba(26, 179, 148, 0.1);
  border-color: rgba(26, 179, 148, 0.3);
}

.item-label {
  flex: 1;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 1rem;
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

.remove-button:hover {
  background-color: #c82333;
}

/* Save Container */
.save-container {
  display: flex;
  justify-content: center;
}

.save-button {
  padding: 0.75rem 2rem;
  background-color: #1ab394;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #148f7a;
}

/* Dialog Customization */
:deep(.p-dialog) {
  border-radius: 16px !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
}

:deep(.p-dialog .p-dialog-header) {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%) !important;
  color: white !important;
  border: none !important;
  padding: 1.5rem !important;
  border-radius: 16px 16px 0 0 !important;
}

:deep(.p-dialog .p-dialog-header .p-dialog-title) {
  font-size: 1.3rem !important;
  font-weight: 700 !important;
  color: white !important;
}

:deep(.p-dialog .p-dialog-content) {
  padding: 2rem !important;
  background-color: #ffffff !important;
}

:deep(.p-dialog-mask.p-component-overlay) {
  background-color: rgba(0, 0, 0, 0.6) !important;
}

/* Form styling */
.create-form-dialog {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  font-size: 0.95rem !important;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 0.75rem !important;
  border: 2px solid rgba(26, 179, 148, 0.2) !important;
  border-radius: 8px !important;
  background-color: #f8f9fa !important;
  font-family: 'Nunito Sans', sans-serif !important;
  transition: all 0.3s !important;
}

.form-input:focus {
  outline: none !important;
  border-color: #1ab394 !important;
  background-color: #ffffff !important;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1) !important;
}

:deep(.form-input.p-inputtext) {
  padding: 0.75rem !important;
  border: 2px solid rgba(26, 179, 148, 0.2) !important;
  border-radius: 8px !important;
  background-color: #f8f9fa !important;
  font-family: 'Nunito Sans', sans-serif !important;
  transition: all 0.3s !important;
}

:deep(.form-input.p-inputtext:focus) {
  outline: none !important;
  border-color: #1ab394 !important;
  background-color: #ffffff !important;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1) !important;
}

:deep(.form-input.p-dropdown) {
  padding: 0.75rem !important;
  border: 2px solid rgba(26, 179, 148, 0.2) !important;
  border-radius: 8px !important;
  background-color: #f8f9fa !important;
  transition: all 0.3s !important;
}

:deep(.form-input.p-dropdown:focus) {
  outline: none !important;
  border-color: #1ab394 !important;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1) !important;
}

:deep(.form-input.p-inputnumber .p-inputnumber-input) {
  padding: 0.75rem !important;
  border: 2px solid rgba(26, 179, 148, 0.2) !important;
  border-radius: 8px !important;
  background-color: #f8f9fa !important;
  transition: all 0.3s !important;
}

:deep(.form-input.p-inputnumber .p-inputnumber-input:focus) {
  outline: none !important;
  border-color: #1ab394 !important;
  background-color: #ffffff !important;
  box-shadow: 0 0 0 3px rgba(26, 179, 148, 0.1) !important;
}

/* Dialog Footer */
:deep(.p-dialog .p-dialog-footer) {
  border-top: 1px solid rgba(26, 179, 148, 0.1) !important;
  padding: 1.5rem 2rem !important;
  background-color: #f8f9fa !important;
  border-radius: 0 0 16px 16px !important;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

:deep(.p-dialog-footer .p-button) {
  font-family: 'Nunito Sans', sans-serif !important;
  font-weight: 600 !important;
}

:deep(.p-dialog-footer .p-button.p-button-secondary) {
  background-color: #e0e0e0 !important;
  color: var(--text-primary) !important;
  border: none !important;
}

:deep(.p-dialog-footer .p-button.p-button-secondary:hover) {
  background-color: #d0d0d0 !important;
}

:deep(.p-dialog-footer .p-button.p-button-success) {
  background: linear-gradient(135deg, #1ab394 0%, #15976d 100%) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(26, 179, 148, 0.3) !important;
}

:deep(.p-dialog-footer .p-button.p-button-success:hover) {
  box-shadow: 0 6px 20px rgba(26, 179, 148, 0.4) !important;
  transform: translateY(-2px) !important;
}
</style>


