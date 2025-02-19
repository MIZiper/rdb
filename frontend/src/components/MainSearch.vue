<template>
  <TagAdder class="pb-0" ref="tagAdder" />
  <v-container class="pt-0">
    <v-btn prepend-icon="mdi-magnify" @click="searchResourcesByTags">Search</v-btn>
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
    async searchResourcesByTags() {
      const selectedTags = this.$refs.tagAdder.selectedTags;
      try {
        const response = await fetch(`http://localhost:5428/resources?tags=${selectedTags.join(';;')}`);
        const data = await response.json();
        // data['items_per_page'] can be [0, int)
        this.$refs.resourceList.setResults(data, this.fetchResources, 1);
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
    async fetchResources(page = 1) {
      try {
        const response = await fetch(`http://localhost:5428/resources?page=${page}`);
        const data = await response.json();
        // data['items_per_page'] > 0
        this.$refs.resourceList.setResults(data, this.fetchResources, page);
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
  },
  created() {
    this.fetchResources();
  }
};
</script>