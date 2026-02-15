import { ref } from 'vue';
import apiClient from '../api/client';

const shoppingListItems = ref([]);
const loading = ref(false);
const error = ref(null);

export function useShoppingList() {
  /**
   * Carrega a lista de compras do usuário
   */
  const fetchShoppingList = async (userEmail) => {
    loading.value = true;
    error.value = null;
    
    try {
      if (!userEmail) {
        shoppingListItems.value = [];
        return [];
      }

      const response = await apiClient.get(`/api/v1/lista-compras/usuario/${userEmail}`);
      shoppingListItems.value = response.data || [];
      return shoppingListItems.value;
      
    } catch (err) {
      console.error('Erro ao buscar lista de compras:', err);
      error.value = err.response?.data?.detail || 'Erro ao carregar lista de compras';
      shoppingListItems.value = [];
      return [];
    } finally {
      loading.value = false;
    }
  };

  /**
   * Adiciona um ingrediente à lista de compras
   */
  const addToShoppingList = async (userEmail, ingredienteId, quantidade = 1) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await apiClient.post(
        `/api/v1/lista-compras/?idIngrediente=${ingredienteId}&idUtilizador=${userEmail}&quantidade=${quantidade}`
      );
      
      // Recarregar a lista após adicionar
      await fetchShoppingList(userEmail);
      
      return response.data;
      
    } catch (err) {
      console.error('Erro ao adicionar à lista de compras:', err);
      error.value = err.response?.data?.detail || 'Erro ao adicionar item';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Remove um item da lista de compras
   */
  const removeFromShoppingList = async (userEmail, ingredienteId) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await apiClient.delete(
        `/api/v1/lista-compras/item/${ingredienteId}/${userEmail}`
      );
      
      // Recarregar a lista após remover
      await fetchShoppingList(userEmail);
      
      return response.data;
      
    } catch (err) {
      console.error('Erro ao remover da lista de compras:', err);
      error.value = err.response?.data?.detail || 'Erro ao remover item';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Limpa toda a lista de compras do usuário
   */
  const clearShoppingList = async (userEmail) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await apiClient.delete(
        `/api/v1/lista-compras/usuario/${userEmail}`
      );
      
      shoppingListItems.value = [];
      return response.data;
      
    } catch (err) {
      console.error('Erro ao limpar lista de compras:', err);
      error.value = err.response?.data?.detail || 'Erro ao limpar lista';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    shoppingListItems,
    loading,
    error,
    fetchShoppingList,
    addToShoppingList,
    removeFromShoppingList,
    clearShoppingList
  };
}
