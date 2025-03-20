<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <component v-if="responseData" :is="dynamicComponent" :data="responseData"></component>
      </v-col>
      <v-col cols="12" md="4">
        <ContentInfoCard v-if="resource" :resource="resource" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ContentInfoCard from './ContentInfoCard.vue';
import MarkdownPage from '../modules/MarkdownPage.vue';
import MermaidDiagram from '../modules/MermaidDiagram.vue';
import { apiClient } from '../config';

export default {
  components: {
    ContentInfoCard,
    MarkdownPage,
    MermaidDiagram,
  },
  data() {
    return {
      dynamicComponent: null,
      responseData: null,
      resource: null,
    };
  },
  created() {
    const resourceId = this.$route.params.resource_id;
    apiClient.get(`/resources/${resourceId}`)
      .then(response => {
        const data = response.data;
        this.resource = data;
        this.responseData = data.content; // Assuming the content is part of the resource data
        this.dynamicComponent = data.type;
      })
      .catch(error => {
        console.error('Error fetching resource:', error);
      });
  },
}
</script>
