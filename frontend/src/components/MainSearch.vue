<template>
  <v-container>
    <TagAdder ref="tagAdder" />
    <v-btn prepend-icon="mdi-magnify" @click="searchResourcesByTags()">Search</v-btn>

    <ResourceList ref="resourceList" />
  </v-container>
</template>

<script>
import TagAdder from './TagAdder.vue';
import ResourceList from './ResourceList.vue';
import { apiClient, TAG_SPLITTER } from '../config';

export default {
  components: {
    TagAdder,
    ResourceList
  },
  methods: {
    async searchResourcesByTags(tags = null) {
      if (tags == null) {
        const selectedTags = this.$refs.tagAdder.selectedTags;
        tags = selectedTags.join(TAG_SPLITTER);
      }
      window.history.replaceState(null, '', `/search?tags=${tags}`);
      try {
        const response = await apiClient.get(`/resources?tags=${tags}`);
        const data = response.data;
        // data['items_per_page'] can be [0, int)
        this.$refs.resourceList.setResults(data, this.fetchResources, 1);
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
    async fetchResources(page = 1) {
      const url = `/resources?page=${page}`;
      window.history.replaceState(null, '', `/search`);
      try {
        const response = await apiClient.get(url);
        const data = response.data;
        // data['items_per_page'] > 0
        this.$refs.resourceList.setResults(data, this.fetchResources, page);
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
  },
  created() {
    const tags = this.$route.query.tags || '';
    if (tags) {
      this.searchResourcesByTags(tags);
    } else {
      this.fetchResources();
    }
  },
};
</script>