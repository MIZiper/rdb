<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="7"
          @update:model-value="handlePageChange"
        ></v-pagination>
      </v-col>
      <v-col cols="12">
        <v-list>
          <v-list-item
            v-for="resource in resources"
            :key="resource.id"
            class="mb-2"
          >
            <v-list-item-content>
              <v-list-item-title>{{ resource.name }}</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  v-for="tag in resource.tags"
                  :key="tag"
                  class="mr-2 mt-2"
                  small
                >
                  {{ tag }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ResourceList',
  data() {
    return {
      resources: []
    }
  },
  methods: {
    async fetchResources() {
      try {
        const response = await fetch('http://localhost:5428/resources')
        const data = await response.json()
        this.resources = data
      } catch (error) {
        console.error('Error fetching resources:', error)
      }
    }
  },
  mounted() {
    this.fetchResources()
  }
}
</script>

<style scoped>
.v-list-item {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}
</style>
