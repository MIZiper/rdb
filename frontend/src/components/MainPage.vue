<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <component :is="dynamicComponent"></component>
      </v-col>
      <v-col cols="12" md="4">
        <ContentViewerTemplate :resource="resource" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ContentViewerTemplate from './ContentViewerTemplate.vue';

export default {
  components: {
    ContentViewerTemplate,
  },
  data() {
    return {
      dynamicComponent: null,
      resource: {
        name: 'Resource Name',
        tags: ['tag1', 'tag2'],
        description: 'What is this?',
        Link2Analysis: 'https://github.com/MIZiper/rdb.git',
        UpdateDate: new Date().toISOString(),
      },
    };
  },
  created() {
    // Logic to set dynamicComponent based on server response
    // this.dynamicComponent = ...
  },
}
</script>
