import { ref } from 'vue';
import apiClient from '@/api/client';

export function useUsers() {
  const users = ref([]);
  const currentUser = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const getUser = async (userId) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/accounts/${userId}`);
      currentUser.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao buscar usuário';
      currentUser.value = null;
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const listUsers = async (limit = 10, offset = 0) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/accounts/', {
        params: { limit, offset },
      });
      users.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao listar usuários';
    } finally {
      loading.value = false;
    }
  };

  const createUser = async (name, email, password) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/accounts/', {
        name,
        email,
        password,
      });
      currentUser.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao criar usuário';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const updateUser = async (userId, name, email) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/accounts/${userId}`, {
        name,
        email,
      });
      currentUser.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao atualizar usuário';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const deleteUser = async (userId) => {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/accounts/${userId}`);
      users.value = users.value.filter((u) => u.id !== userId);
      currentUser.value = null;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Erro ao deletar usuário';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    currentUser,
    loading,
    error,
    getUser,
    listUsers,
    createUser,
    updateUser,
    deleteUser,
  };
}
