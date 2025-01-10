<template>
  <v-container>
    <v-autocomplete
      v-model="searchQuery"
      :items="allTags"
      label="Search"
      prepend-icon="mdi-magnify"
      clearable
      multiple
      chips
    ></v-autocomplete>
    <v-row justify="space-between" align="center">
      <v-col>
        <p>{{ results.length }} results found</p>
      </v-col>
      <v-col cols="auto" class="d-flex align-center">
        <v-pagination
          v-model="page"
          :length="pageCount"
          :total-visible="5"
        ></v-pagination>
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
      <v-list-item
        v-for="(result, index) in paginatedResults"
        :key="index"
      >
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
          <v-chip-group>
            <v-chip
              v-for="(tag, tagIndex) in result.tags"
              :key="tagIndex"
            >
              {{ tag }}
            </v-chip>
          </v-chip-group>
        </v-list-item-content>
        <v-divider v-if="index < paginatedResults.length - 1"></v-divider>
      </v-list-item>
    </v-list>
    <v-row justify="end">
      <v-pagination
        v-model="page"
        :length="pageCount"
        :total-visible="5"
      ></v-pagination>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: [],
      allTags: [
        'apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'kiwi', 'lemon',
        'mango', 'nectarine', 'orange', 'papaya', 'quince', 'raspberry', 'strawberry', 'tangerine', 'ugli', 'vanilla',
        'watermelon', 'xigua'
      ],
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
    }
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