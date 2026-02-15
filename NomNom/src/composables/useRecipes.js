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
      // Se não há email, não há receitas favoritas ainda
      if (!userEmail) {
        minhasReceitas.value = [];
        return;
      }

      const response = await apiClient.get('/api/v1/receitas/minhas', {
        params: { user_email: userEmail }
      });
      minhasReceitas.value = response.data || [];
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar minhas receitas';
      console.error('Erro ao buscar minhas receitas:', err);
      minhasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchOutrasReceitas = async (userEmail = null) => {
    loading.value = true;
    error.value = null;
    try {
      if (!userEmail) {
        const response = await apiClient.get('/api/v1/receitas');
        outrasReceitas.value = response.data || [];
        return;
      }

      const response = await apiClient.get('/api/v1/receitas/outras', {
        params: { user_email: userEmail }
      });
      outrasReceitas.value = response.data || [];
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar outras receitas';
      console.error('Erro ao buscar outras receitas:', err);
      outrasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchOutrasReceitasWithFilters = async (userEmail = null, filters = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const params = {};
      
      // Add user email
      if (userEmail) {
        params.user_email = userEmail;
      }
      
      // Add filters
      if (filters.dificuldade) {
        params.dificuldade = filters.dificuldade;
      }
      if (filters.categoria) {
        params.categoria = filters.categoria;
      }
      if (filters.tipo_cozinhado) {
        params.tipo_cozinhado = filters.tipo_cozinhado;
      }
      if (filters.tempo_min !== undefined && filters.tempo_min !== null) {
        params.tempo_min = filters.tempo_min;
      }
      if (filters.tempo_max !== undefined && filters.tempo_max !== null) {
        params.tempo_max = filters.tempo_max;
      }
      if (filters.porcoes_min !== undefined && filters.porcoes_min !== null) {
        params.porcoes_min = filters.porcoes_min;
      }
      if (filters.porcoes_max !== undefined && filters.porcoes_max !== null) {
        params.porcoes_max = filters.porcoes_max;
      }
      if (filters.onlyMyIngredients) {
        params.only_my_ingredients = true;
      }

      const response = await apiClient.get('/api/v1/receitas/outras/filtradas', {
        params: params
      });
      outrasReceitas.value = response.data || [];
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar receitas filtradas';
      console.error('Erro ao buscar receitas filtradas:', err);
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
        fetchOutrasReceitas(userEmail)
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
    fetchOutrasReceitasWithFilters,
    fetchTodasReceitas,
    fetchAllRecipes
  };
}
