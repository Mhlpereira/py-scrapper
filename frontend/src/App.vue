<template background="#F5EEDC">
  <div class="container mx-auto p-4">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold mb-2">Consulta de Operadoras ANS</h1>
      <p class="text-gray-600 mb-6">
        Pesquise informações sobre operadoras de planos de saúde ativas na ANS
      </p>

      <div class="flex max-w-md mx-auto">
        <input
          v-model="searchQuery"
          @keyup.enter="searchOperators"
          type="text"
          class="flex-grow px-4 py-2 border border-gray-300 rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Digite o nome da operadora, cidade ou UF..."
        />
        <button
          @click="searchOperators"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-r transition-colors"
          :disabled="loading"
        >
          {{ loading ? "Buscando..." : "Buscar" }}
        </button>
      </div>
    </div>

    <!-- Loading spinner -->
    <div v-if="loading" class="flex justify-center my-8">
      <spinner-component />
    </div>

    <!-- Error message -->
    <error-message v-if="error" :message="error" @close="error = null" />

    <!-- Results section -->
    <results-table v-if="results.length > 0 && !loading" :results="results" />

    <empty-state v-if="results.length === 0 && !loading && searched" />
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import SpinnerComponent from "./components/SpinnerComponent.vue";
import ErrorMessage from "./components/ErrorMessage.vue";
import ResultsTable from "./components/ResultsTable.vue";
import EmptyState from "./components/EmptyState.vue";

export default {
  name: "App",
  components: {
    SpinnerComponent,
    ErrorMessage,
    ResultsTable,
    EmptyState,
  },
  setup() {
    const API_URL = "http://localhost:8000/api/operadoras";

    const searchQuery = ref("");
    const results = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const searched = ref(false);

    const searchOperators = async () => {
      if (!searchQuery.value.trim()) {
        error.value = "Por favor, digite um termo para pesquisa.";
        return;
      }

      loading.value = true;
      error.value = null;
      searched.value = true;

      try {
        const response = await axios.get(`${API_URL}/search`, {
          params: { q: searchQuery.value },
        });

        results.value = response.data.results;
      } catch (err) {
        console.error("Search error:", err);
        error.value =
          err.response?.data?.detail ||
          "Erro ao buscar operadoras. Tente novamente.";
        results.value = [];
      } finally {
        loading.value = false;
      }
    };

    return {
      searchQuery,
      results,
      loading,
      error,
      searched,
      searchOperators,
    };
  },
};
</script>
