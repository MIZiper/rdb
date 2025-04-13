<template>
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
            <a :href="`/resources/${result.uuid || ''}`">
              <v-list-item-title>{{ result.title }}</v-list-item-title>
            </a>
          </v-col>
          <v-col cols="auto">
            <v-icon small class="mr-1">mdi-calendar</v-icon>
            <small>{{ new Date(result.update_date).toLocaleString() }}</small>
          </v-col>
        </v-row>
        <v-list-item-subtitle class="ma-3">{{ result.description || '[No description]' }}</v-list-item-subtitle>
        <v-row class="ma-0">
          <a v-for="(tag, tagIndex) in result.tags.split(TAG_SPLITTER)" :key="tagIndex" :href="`/search?tags=${tag}`">
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
</template>

<script>
import { getTagColor } from './utils'; // Import the getTagColor function
import { TAG_SPLITTER } from '../config';

export default {
  data() {
    return {
      results: [],
      page: 1,
      totalItems: 0,
      itemsPerPage: 7,
      sortOrder: 'None',
      paginationCB: null,
      TAG_SPLITTER: TAG_SPLITTER,
    };
  },
  methods: {
    toggleSortOrder() {
      if (this.sortOrder === 'None' || this.sortOrder === 'Descending') {
        this.sortOrder = 'Ascending';
        this.results.sort((a, b) => new Date(a.update_date) - new Date(b.update_date));
      } else {
        this.sortOrder = 'Descending';
        this.results.sort((a, b) => new Date(b.update_date) - new Date(a.update_date));
      }
    },
    setResults(data, dynamic_cb = null, page = 1) {
      this.results = data['resources'];
      this.totalItems = data['total_resources'];
      this.page = Number(page);
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
.v-list-item a {
  text-decoration: none;
  color: black;
}
</style>
