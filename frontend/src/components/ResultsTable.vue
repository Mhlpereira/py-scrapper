<template>
  <div class="mt-6">
    <h2 class="text-xl font-semibold mb-4">
      Resultados da Pesquisa ({{ results.length }})
    </h2>

    <div class="overflow-x-auto shadow-md rounded-lg">
      <table class="min-w-full bg-white">
        <thead>
          <tr class="bg-gray-100 border-b">
            <th
              v-for="column in columns"
              :key="column.key"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr
            v-for="(item, index) in results"
            :key="index"
            class="hover:bg-gray-50"
          >
            <td
              class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
            >
              {{ item.registro_ans }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-900">
              {{ item.razao_social }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-900">
              {{ item.nome_fantasia }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-900">
              {{ item.cidade }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ item.uf }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
  setup() {
    const columns = [
      { key: "registro_ans", label: "Registro ANS" },
      { key: "razao_social", label: "Razão Social" },
      { key: "nome_fantasia", label: "Nome Fantasia" },
      { key: "cidade", label: "Cidade" },
      { key: "uf", label: "UF" },
    ];

    return {
      columns,
    };
  },
};
</script>
