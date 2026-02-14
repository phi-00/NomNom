import { ref, computed } from 'vue';
import apiClient from '../api/client';

export function useRecipes() {
  const minhasReceitas = ref([]);
  const outrasReceitas = ref([]);
  const todasReceitas = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchMinhasReceitas = async (userEmail = null) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/receitas/minhas');
      minhasReceitas.value = response.data || [];
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar minhas receitas';
      console.error('Erro ao buscar minhas receitas:', err);
      minhasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchOutrasReceitas = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/receitas/outras');
      outrasReceitas.value = response.data || [];
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar outras receitas';
      console.error('Erro ao buscar outras receitas:', err);
      outrasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchTodasReceitas = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/receitas');
      todasReceitas.value = response.data || [];
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar receitas';
      console.error('Erro ao buscar receitas:', err);
      todasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchAllRecipes = async (userEmail = null) => {
    loading.value = true;
    error.value = null;
    try {
      await Promise.all([
        fetchMinhasReceitas(userEmail),
        fetchOutrasReceitas()
      ]);
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar receitas';
      console.error('Erro ao buscar receitas:', err);
    } finally {
      loading.value = false;
    }
  };

  return {
    minhasReceitas,
    outrasReceitas,
    todasReceitas,
    loading,
    error,
    fetchMinhasReceitas,
    fetchOutrasReceitas,
    fetchTodasReceitas,
    fetchAllRecipes
  };
}
