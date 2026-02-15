<template>
  <section class="profile">
    <div class="profile-container">
      <h1>My Profile</h1>
      <p class="subtitle">View your profile information</p>

      <div class="profile-card">
        <!-- Profile Picture -->
        <div class="profile-picture-section">
          <div class="picture-wrapper">
            <img 
              v-if="profilePicture" 
              :src="profilePicture" 
              :alt="userName"
              class="profile-picture"
            />
            <div v-else class="picture-placeholder">👤</div>
          </div>
        </div>

        <!-- User Information -->
        <div class="user-info-section">
          <!-- Email (read-only) -->
          <div class="info-field">
            <label>Email:</label>
            <div class="field-value">{{ userEmail }}</div>
          </div>

          <!-- Username (read-only) -->
          <div class="info-field">
            <label>Username:</label>
            <div class="field-value">{{ userName }}</div>
          </div>

          <!-- Member Since -->
          <div class="info-field">
            <label>Member Since:</label>
            <div class="field-value">{{ formatDate(userCreatedAt) }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const user = ref(null);
const profilePicture = ref(null);

const userName = computed(() => {
  return user.value?.name || 'User';
});

const userEmail = computed(() => {
  return user.value?.email || 'email@example.com';
});

const userCreatedAt = computed(() => {
  return user.value?.created_at || null;
});

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

onMounted(() => {
  loadUserData();
});

const loadUserData = () => {
  const userData = localStorage.getItem('user');
  if (userData) {
    try {
      user.value = JSON.parse(userData);
      profilePicture.value = user.value?.profile_picture || null;
    } catch (e) {
      console.error('Error parsing user data:', e);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700&display=swap');

.profile {
  padding: 2rem;
  min-height: 100vh;
  font-family: 'Nunito Sans';
  background: var(--bg-card);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-container {
  max-width: 700px;
  margin: 0 auto;
}

h1 {
  color: #1ab394;
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
}

.subtitle {
  color: #454545;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.profile-card {
  background: var(--bg-card);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
  padding: 2.5rem;
  margin-bottom: 2rem;
  border: 1px solid #1ab394;
}

/* Profile Picture Section */
.profile-picture-section {
  text-align: center;
  margin-bottom: 2.5rem;
  padding-bottom: 2.5rem;
  border-bottom: 2px solid rgba(26, 179, 148, 0.2);
}

.picture-wrapper {
  margin-bottom: 1.5rem;
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #1ab394;
  display: block;
  margin: 0 auto;
}

.picture-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e8f5f0 0%, #d0f0e8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  margin: 0 auto;
  border: 4px solid #ddd;
}

/* User Information Section */
.user-info-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-field label {
  color: #1ab394;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.field-value {
  color: var(--text-primary);
  font-size: 1rem;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  word-break: break-all;
  border: 1px solid rgba(26, 179, 148, 0.15);
}

/* Responsive */
@media (max-width: 768px) {
  .profile {
    padding: 1rem;
  }

  .profile-card {
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  .profile-picture {
    width: 100px;
    height: 100px;
  }

  .picture-placeholder {
    width: 100px;
    height: 100px;
    font-size: 2.5rem;
  }
}
</style>
