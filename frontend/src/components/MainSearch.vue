<template>
  <TagAdder class="pb-0" ref="tagAdder" />
  <v-container class="pt-0">
    <v-btn prepend-icon="mdi-magnify" @click="searchResourcesByTags()">Search</v-btn>
  </v-container>
  <ResourceList ref="resourceList" />
</template>

<script>
import TagAdder from './TagAdder.vue';
import ResourceList from './ResourceList.vue';

export default {
  components: {
    TagAdder,
    ResourceList
  },
  methods: {
    async searchResourcesByTags(tags = null) {
      if (tags == null) {
        const selectedTags = this.$refs.tagAdder.selectedTags;
        tags = selectedTags.join(';;');
      }
      this.$router.push({ path: '/resources', query: { tags } });
      try {
        const response = await fetch(`http://localhost:5428/resources?tags=${tags}`);
        const data = await response.json();
        // data['items_per_page'] can be [0, int)
        this.$refs.resourceList.setResults(data, this.fetchResources, 1);
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
    async fetchResources(page = 1) {
      // const tags = this.$route.query.tags || '';
      // const url = tags ? `http://localhost:5428/resources?tags=${tags}&page=${page}` : `http://localhost:5428/resources?page=${page}`;
      const url = `http://localhost:5428/resources?page=${page}`;
      this.$router.push({ path: '/resources', query: { page } });
      try {
        const response = await fetch(url);
        const data = await response.json();
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
  watch: {
    '$route.query.tags': function(newTags) {
      if (newTags) {
        this.searchResourcesByTags(newTags);
      } else {
        this.fetchResources();
      }
    },
    '$route.query.page': function(newPage) {
      this.fetchResources(newPage);
    }
  }
};
</script>