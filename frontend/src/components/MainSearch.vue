<template>
    <TagAdder class="pb-0" ref="tagAdder"/>
    <v-container class="pt-0">
        <v-btn prepend-icon="mdi-magnify" @click="searchResources">Search</v-btn>
    </v-container>
    <ResourceList ref="resourceList"/>
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
    async searchResources() {
      const selectedTags = this.$refs.tagAdder.selectedTags;
      try {
        const response = await fetch(`http://localhost:5428/resources?tags=${selectedTags.join(';;')}`);
        const data = await response.json();
        this.$refs.resourceList.results = data['resources'].map(resource => ({
          title: resource.name,
          description: resource.description || '',
          tags: resource.tags,
          modifiedDate: resource.modifiedDate
        }));
        this.$refs.resourceList.totalItems = data['total_resources'];
        this.$refs.resourceList.page = 1;
        this.$refs.resourceList.itemsPerPage = 7;
        this.$refs.resourceList.paginationMode = 'static';
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    }
  }
};
</script>