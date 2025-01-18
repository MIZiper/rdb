<template>
  <div>
    <v-row class="ma-0">
      <v-chip v-for="(tag, index) in selectedTags" :key="index" closable>
        {{ tag }}
      </v-chip>
    </v-row>
    <v-text-field v-model="search" label="Add tag" clearable @keydown.enter="addTag" @input="onChange(search)"
      @focus="onFocus" ref="searchField"></v-text-field>
    <v-menu v-model="menu" :close-on-content-click="false" :offset-y="true">
      <v-list>
        <v-list-item v-for="(tag, index) in filteredTags" :key="index" @click="selectTag(tag)">
          <v-list-item-title>{{ tag }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      search: '',
      currentScopeTags: [],
      filteredTags: [],
      selectedTags: [],
      loading: false,
      menu: false,
    };
  },
  methods: {
    async fetchTags(parentTag = '') {
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:5428/tags/${parentTag}`);
        this.currentScopeTags = response.data;
        this.filteredTags = this.currentScopeTags;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    onChange(val) {
      let currentScopeTag = '';
      if (val.endsWith(':')) {
        const parentTag = val.split(':').slice(0, -1).join(':');
        this.fetchTags(parentTag);
      } else {
        currentScopeTag = val.split(':').slice(-1)[0];
      }

      if (!currentScopeTag) {
        this.filteredTags = this.currentScopeTags;
      } else {
        this.filteredTags = this.currentScopeTags.filter(tag => tag.includes(currentScopeTag));
      }
    },
    addTag() {
      if (this.search && !this.selectedTags.includes(this.search)) {
        this.selectedTags.push(this.search);
        this.search = '';
      }
    },
    selectTag(tag) {
      const parentTag = this.search.split(':').slice(0, -1).join(':');
      if (parentTag) {
        this.search = `${parentTag}:${tag}`;
      } else {
        this.search = tag;
      }
      this.menu = false;
    },
    onFocus(focus) {
      if (focus) {
        this.menu = true;
      }
    },
  },
  mounted() {
    this.fetchTags();
  },
};
</script>
