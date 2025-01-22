<template>
  <v-container>
    <v-row justify="space-between" align="center">
      <v-col>
        <p>{{ results.length }} results found</p>
      </v-col>
      <v-col cols="auto" class="d-flex align-center">
        <v-pagination v-model="page" :length="pageCount" :total-visible="5"></v-pagination>
        <v-btn icon @click="toggleSortOrder" class="ml-3">
          <v-icon>
            {{
              sortOrder === 'None'
                ? 'mdi-sort'
                : sortOrder === 'Descending'
                  ? 'mdi-arrow-down'
                  : 'mdi-arrow-up'
            }}
          </v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-list>
      <v-list-item v-for="(result, index) in paginatedResults" :key="index" class="mb-2">
        <v-list-item-content>
          <v-row justify="space-between" align="center">
            <v-col>
              <v-list-item-title>{{ result.title }}</v-list-item-title>
            </v-col>
            <v-col cols="auto" class="d-flex align-center">
              <v-icon small class="mr-1">mdi-calendar</v-icon>
              <small>{{ result.modifiedDate }}</small>
            </v-col>
          </v-row>
          <v-list-item-subtitle class="ma-3">{{ result.description }}</v-list-item-subtitle>
          <v-row class="ma-0">
            <a v-for="(tag, tagIndex) in result.tags" :key="tagIndex" :href="`/search?tag=${tag}`" target="_blank">
              <v-chip :color="getTagColor(tag)" class="mr-1 mb-1">
                {{ tag }}
              </v-chip>
            </a>
          </v-row>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-row justify="end">
      <v-pagination v-model="page" :length="pageCount" :total-visible="5"></v-pagination>
    </v-row>
  </v-container>
</template>

<script>
import { getTagColor } from './utils'; // Import the getTagColor function

export default {
  data() {
    return {
      results: [
        {
          title: 'Sample Result 1',
          description: 'Description for Sample Result 1',
          tags: ['apple', 'banana'],
          modifiedDate: '2023-10-01'
        },
        {
          title: 'Sample Result 2',
          description: 'Description for Sample Result 2',
          tags: ['cherry', 'date'],
          modifiedDate: '2023-10-02'
        },
        {
          title: 'Sample Result 3',
          description: 'Description for Sample Result 3',
          tags: ['elderberry', 'fig'],
          modifiedDate: '2023-10-03'
        },
        {
          title: 'Sample Result 4',
          description: 'Description for Sample Result 4',
          tags: ['grape', 'honeydew'],
          modifiedDate: '2023-10-04'
        },
        {
          title: 'Sample Result 5',
          description: 'Description for Sample Result 5',
          tags: ['kiwi', 'lemon'],
          modifiedDate: '2023-10-05'
        },
        {
          title: 'Sample Result 6',
          description: 'Description for Sample Result 6',
          tags: ['mango', 'nectarine'],
          modifiedDate: '2023-10-06'
        },
        {
          title: 'Sample Result 7',
          description: 'Description for Sample Result 7',
          tags: ['orange', 'papaya'],
          modifiedDate: '2023-10-07'
        },
        {
          title: 'Sample Result 8',
          description: 'Description for Sample Result 8',
          tags: ['quince', 'raspberry'],
          modifiedDate: '2023-10-08'
        },
        {
          title: 'Sample Result 9',
          description: 'Description for Sample Result 9',
          tags: ['strawberry', 'tangerine'],
          modifiedDate: '2023-10-09'
        },
        {
          title: 'Sample Result 10',
          description: 'Description for Sample Result 10',
          tags: ['ugli', 'vanilla'],
          modifiedDate: '2023-10-10'
        },
        {
          title: 'Sample Result 11',
          description: 'Description for Sample Result 11',
          tags: ['watermelon', 'xigua'],
          modifiedDate: '2023-10-11'
        },
      ],
      page: 1,
      itemsPerPage: 7,
      sortOrder: 'None'
    };
  },
  methods: {
    toggleSortOrder() {
      if (this.sortOrder === 'None' || this.sortOrder === 'Descending') {
        this.sortOrder = 'Ascending';
        this.results.sort((a, b) => new Date(a.modifiedDate) - new Date(b.modifiedDate));
      } else {
        this.sortOrder = 'Descending';
        this.results.sort((a, b) => new Date(b.modifiedDate) - new Date(a.modifiedDate));
      }
    },
    async fetchResources() {
      try {
        const response = await fetch('http://localhost:5428/resources');
        const data = await response.json();
        this.results = data.map(resource => ({
          title: resource.name,
          description: resource.description || '',
          tags: resource.tags,
          modifiedDate: resource.modifiedDate
        }));
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
    getTagColor // Add getTagColor to methods
  },
  created() {
    this.fetchResources();
  },
  computed: {
    pageCount() {
      return Math.ceil(this.results.length / this.itemsPerPage);
    },
    paginatedResults() {
      const start = (this.page - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.results.slice(start, end);
    }
  }
};
</script>

<style scoped>
.v-list-item {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}
</style>
