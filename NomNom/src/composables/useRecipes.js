import { ref, computed } from 'vue';
import apiClient from '../api/client';

// Shared state with caching
const minhasReceitas = ref([]);
const outrasReceitas = ref([]);
const todasReceitas = ref([]);
const loading = ref(false);
const error = ref(null);

// Cache timestamps to avoid refetching too frequently
const cache = {
  minhasReceitas: { timestamp: 0, userEmail: null },
  outrasReceitas: { timestamp: 0, userEmail: null, filters: null },
  todasReceitas: { timestamp: 0 }
};

const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

export function useRecipes() {
  const isCacheValid = (cacheKey) => {
    const now = Date.now();
    return (now - cache[cacheKey].timestamp) < CACHE_DURATION;
  };

  const fetchMinhasReceitas = async (userEmail = null, forceRefresh = false) => {
    // Check cache
    if (!forceRefresh && 
        isCacheValid('minhasReceitas') && 
        cache.minhasReceitas.userEmail === userEmail &&
        minhasReceitas.value.length > 0) {
      console.log('Using cached minhas receitas');
      return minhasReceitas.value;
    }

    loading.value = true;
    error.value = null;
    try {
      // Se não há email, não há receitas favoritas ainda
      if (!userEmail) {
        minhasReceitas.value = [];
        cache.minhasReceitas.timestamp = Date.now();
        cache.minhasReceitas.userEmail = null;
        return;
      }

      console.log('Fetching minhas receitas from API...');
      const response = await apiClient.get('/api/v1/receitas/minhas', {
        params: { user_email: userEmail }
      });
      minhasReceitas.value = response.data || [];
      cache.minhasReceitas.timestamp = Date.now();
      cache.minhasReceitas.userEmail = userEmail;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar minhas receitas';
      console.error('Erro ao buscar minhas receitas:', err);
      minhasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchOutrasReceitas = async (userEmail = null, forceRefresh = false) => {
    // Check cache
    if (!forceRefresh && 
        isCacheValid('outrasReceitas') && 
        cache.outrasReceitas.userEmail === userEmail &&
        outrasReceitas.value.length > 0) {
      console.log('Using cached outras receitas');
      return outrasReceitas.value;
    }

    loading.value = true;
    error.value = null;
    try {
      console.log('Fetching outras receitas from API...');
      if (!userEmail) {
        const response = await apiClient.get('/api/v1/receitas');
        outrasReceitas.value = response.data || [];
        cache.outrasReceitas.timestamp = Date.now();
        cache.outrasReceitas.userEmail = null;
        return;
      }

      const response = await apiClient.get('/api/v1/receitas/outras', {
        params: { user_email: userEmail }
      });
      outrasReceitas.value = response.data || [];
      cache.outrasReceitas.timestamp = Date.now();
      cache.outrasReceitas.userEmail = userEmail;
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

      console.log('Fetching outras receitas with filters from API...', params);
      const response = await apiClient.get('/api/v1/receitas/outras/filtradas', {
        params: params
      });
      outrasReceitas.value = response.data || [];
      
      // Update cache when no filters or only user_email
      if (Object.keys(filters).length === 0 || 
          (Object.keys(filters).length === 1 && filters.onlyMyIngredients === false)) {
        cache.outrasReceitas.timestamp = Date.now();
        cache.outrasReceitas.userEmail = userEmail;
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar receitas filtradas';
      console.error('Erro ao buscar receitas filtradas:', err);
      outrasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const fetchTodasReceitas = async (forceRefresh = false) => {
    // Check cache
    if (!forceRefresh && 
        isCacheValid('todasReceitas') &&
        todasReceitas.value.length > 0) {
      console.log('Using cached todas receitas');
      return todasReceitas.value;
    }

    loading.value = true;
    error.value = null;
    try {
      console.log('Fetching todas receitas from API...');
      const response = await apiClient.get('/api/v1/receitas');
      todasReceitas.value = response.data || [];
      cache.todasReceitas.timestamp = Date.now();
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar receitas';
      console.error('Erro ao buscar receitas:', err);
      todasReceitas.value = [];
    } finally {
      loading.value = false;
    }
  };

  const clearCache = () => {
    console.log('Clearing recipes cache');
    cache.minhasReceitas.timestamp = 0;
    cache.outrasReceitas.timestamp = 0;
    cache.todasReceitas.timestamp = 0;
  };

  const fetchAllRecipes = async (userEmail = null, forceRefresh = false) => {
    loading.value = true;
    error.value = null;
    try {
      console.log('Fetching all recipes...');
      await Promise.all([
        fetchMinhasReceitas(userEmail, forceRefresh),
        fetchOutrasReceitas(userEmail, forceRefresh)
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
    fetchAllRecipes,
    clearCache
  };
}
