<template>
  <v-container>
    <v-row class="align-center">
      <v-col>
        <p>{{ totalItems }} results found</p>
      </v-col>
      <v-col cols="auto" class="d-flex align-center">
        <v-pagination v-model="page" :length="pageCount" :total-visible="5"
          @update:modelValue="onPageChange"></v-pagination>
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
        <v-row>
          <v-col>
            <v-list-item-title>{{ result.title }}</v-list-item-title>
          </v-col>
          <v-col cols="auto">
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
      </v-list-item>
    </v-list>
    <v-row justify="end">
      <v-pagination v-model="page" :length="pageCount" :total-visible="5"
        @update:modelValue="onPageChange"></v-pagination>
    </v-row>
  </v-container>
</template>

<script>
import { getTagColor } from './utils'; // Import the getTagColor function

export default {
  data() {
    return {
      results: [],
      page: 1,
      totalItems: 0,
      itemsPerPage: 7,
      sortOrder: 'None',
      paginationCB: null,
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
    setResults(data, dynamic_cb = null, page = 1) {
      this.results = data['resources'].map(resource => ({
        title: resource.name,
        description: resource.description || '[No description]',
        tags: resource.tags,
        modifiedDate: resource.modifiedDate
      }));
      this.totalItems = data['total_resources'];
      this.page = page;
      if (data['items_per_page'] == 0) {
        this.itemsPerPage = 7;
        this.paginationCB = null;
      } else {
        this.itemsPerPage = data['items_per_page'];
        this.paginationCB = dynamic_cb;
      }
    },
    getTagColor, // Add getTagColor to methods
    onPageChange() {
      if (this.paginationCB) {
        this.paginationCB(this.page);
      }
    }
  },
  created() {
    const example = [
      {
        name: 'Sample Result 1',
        description: 'Description for Sample Result 1',
        tags: ['apple', 'banana'],
        modifiedDate: '2023-10-01'
      },
      {
        name: 'Sample Result 2',
        description: 'Description for Sample Result 2',
        tags: ['cherry', 'date'],
        modifiedDate: '2023-10-02'
      },
      {
        name: 'Sample Result 3',
        description: 'Description for Sample Result 3',
        tags: ['elderberry', 'fig'],
        modifiedDate: '2023-10-03'
      },
      {
        name: 'Sample Result 4',
        description: 'Description for Sample Result 4',
        tags: ['grape', 'honeydew'],
        modifiedDate: '2023-10-04'
      },
      {
        name: 'Sample Result 5',
        description: 'Description for Sample Result 5',
        tags: ['kiwi', 'lemon'],
        modifiedDate: '2023-10-05'
      },
      {
        name: 'Sample Result 6',
        description: 'Description for Sample Result 6',
        tags: ['mango', 'nectarine'],
        modifiedDate: '2023-10-06'
      },
      {
        name: 'Sample Result 7',
        description: 'Description for Sample Result 7',
        tags: ['orange', 'papaya'],
        modifiedDate: '2023-10-07'
      },
      {
        name: 'Sample Result 8',
        description: 'Description for Sample Result 8',
        tags: ['quince', 'raspberry'],
        modifiedDate: '2023-10-08'
      },
      {
        name: 'Sample Result 9',
        description: 'Description for Sample Result 9',
        tags: ['strawberry', 'tangerine'],
        modifiedDate: '2023-10-09'
      },
      {
        name: 'Sample Result 10',
        description: 'Description for Sample Result 10',
        tags: ['ugli', 'vanilla'],
        modifiedDate: '2023-10-10'
      },
      {
        name: 'Sample Result 11',
        description: 'Description for Sample Result 11',
        tags: ['watermelon', 'xigua'],
        modifiedDate: '2023-10-11'
      },
    ];

    this.setResults(
      { resources: example, total_resources: example.length, items_per_page: 0 },
    )
  },
  computed: {
    pageCount() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    paginatedResults() {
      if (!this.paginationCB) {
        const start = (this.page - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.results.slice(start, end);
      }
      return this.results;
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
