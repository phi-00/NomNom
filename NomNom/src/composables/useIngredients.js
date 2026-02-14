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
  };
}
