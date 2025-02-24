<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <component :is="dynamicComponent" :data="responseData"></component>
      </v-col>
      <v-col cols="12" md="4">
        <ContentViewerTemplate :resource="resource" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ContentViewerTemplate from './ContentViewerTemplate.vue';
import MarkdownPage from '../modules/MarkdownPage.vue';
import MermaidDiagram from '../modules/MermaidDiagram.vue';

export default {
  components: {
    ContentViewerTemplate,
    MarkdownPage,
    MermaidDiagram,
  },
  data() {
    return {
      dynamicComponent: null,
      responseData: null,
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
    // Simulate server response
    const serverResponse = {
      type: 'mermaid', // or 'markdown'
      data: `
        graph TD;
          A-->B;
          A-->C;
          B-->D;
          C-->D;
      `,
    };

    this.responseData = serverResponse.data;

    if (serverResponse.type === 'markdown') {
      this.dynamicComponent = 'MarkdownPage';
    } else if (serverResponse.type === 'mermaid') {
      this.dynamicComponent = 'MermaidDiagram';
    }
  },
}
</script>
