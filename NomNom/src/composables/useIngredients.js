import { ref, computed } from 'vue';
import apiClient from '../api/client';

export function useIngredients() {
  const columns = ref([]);
  const ingredientes = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const preview = ref([]);

  const totalColumns = computed(() => columns.value.length);

  const fetchColumns = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/ingredientes/columns');
      columns.value = response.data.columns;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar colunas';
      console.error('Erro ao buscar colunas:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchPreview = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/ingredientes/preview');
      columns.value = response.data.columns;
      preview.value = response.data.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar preview';
      console.error('Erro ao buscar preview:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchIngredientes = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/ingredientes');
      ingredientes.value = response.data;
      
      // Se response.data é um array com dados, extrair as colunas
      if (response.data && response.data.length > 0) {
        const keys = Object.keys(response.data[0]);
        columns.value = keys.map(key => ({ column_name: key }));
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar ingredientes';
      console.error('Erro ao buscar ingredientes:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchUserInventory = async (userEmail) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/v1/ingredientes/inventario/${userEmail}`);
      ingredientes.value = response.data;
      
      // Se response.data é um array com dados, extrair as colunas
      if (response.data && response.data.length > 0) {
        const keys = Object.keys(response.data[0]);
        columns.value = keys.map(key => ({ column_name: key }));
      }
      
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar inventário';
      console.error('Erro ao buscar inventário:', err);
      return [];
    } finally {
      loading.value = false;
    }
  };

  const searchIngredientByName = async (name) => {
    try {
      const response = await apiClient.get('/api/v1/ingredientes');
      const allIngredients = response.data;
      
      // Search for ingredient by name (case insensitive)
      return allIngredients.find(ing => 
        ing.nome.toLowerCase() === name.toLowerCase()
      );
    } catch (err) {
      console.error('Erro ao buscar ingrediente:', err);
      return null;
    }
  };

  const searchSimilarIngredients = async (name) => {
    try {
      const response = await apiClient.get('/api/v1/ingredientes');
      const allIngredients = response.data;
      
      // Fuzzy search - find ingredients that contain the search term
      return allIngredients.filter(ing => 
        ing.nome.toLowerCase().includes(name.toLowerCase()) ||
        name.toLowerCase().includes(ing.nome.toLowerCase())
      ).slice(0, 10); // Limit to 10 results
    } catch (err) {
      console.error('Erro ao buscar ingredientes similares:', err);
      return [];
    }
  };

  const createIngredient = async (ingredientData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/api/v1/ingredientes', ingredientData);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao criar ingrediente';
      console.error('Erro ao criar ingrediente:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const addToInventory = async (userEmail, ingredientId, quantity = 1) => {
    loading.value = true;
    error.value = null;
    try {
      const payload = {
        idUtilizador: userEmail,
        idIngrediente: Number(ingredientId),
        quantidade: Number(quantity)
      };
      
      const response = await apiClient.post('/api/v1/ingredientes/inventario', payload);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao adicionar ao inventário';
      console.error('Erro ao adicionar ao inventário:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateInventoryQuantity = async (userEmail, ingredientId, newQuantity) => {
    loading.value = true;
    error.value = null;
    try {
      const payload = {
        idUtilizador: userEmail,
        idIngrediente: Number(ingredientId),
        quantidade: Number(newQuantity)
      };
      
      const response = await apiClient.patch('/api/v1/ingredientes/inventario', payload);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao atualizar quantidade';
      console.error('Erro ao atualizar quantidade:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const removeFromInventory = async (userEmail, ingredientId) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.delete('/api/v1/ingredientes/inventario', {
        data: {
          idUtilizador: userEmail,
          idIngrediente: Number(ingredientId)
        }
      });
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao remover do inventário';
      console.error('Erro ao remover do inventário:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    columns,
    ingredientes,
    preview,
    loading,
    error,
    totalColumns,
    fetchColumns,
    fetchPreview,
    fetchIngredientes,
    fetchUserInventory,
    searchIngredientByName,
    searchSimilarIngredients,
    createIngredient,
    addToInventory,
    updateInventoryQuantity,
    removeFromInventory,
  };
}
