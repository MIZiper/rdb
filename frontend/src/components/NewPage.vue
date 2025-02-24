<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-select label="Resource Types" v-model="dynamicComponent" :items="AvailableModules" item-title="title" item-value="vueName"></v-select>
        <component v-if="dynamicComponent" :editMode="true" :is="dynamicComponent" :data="requestData"></component>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>New Resource</v-card-title>
          <v-card-text>
            <v-text-field density="compact" v-model="resource.name" label="Name"></v-text-field>
            <v-text-field density="compact" v-model="resource.link" label="Link"></v-text-field>
            <v-textarea density="compact" v-model="resource.description" label="Description"></v-textarea>

            <v-divider />
            <div class="text-subtitle-1 font-weight-medium">Tags:</div>
            <TagAdder />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" variant="outlined">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MarkdownPage from '../modules/MarkdownPage.vue';
import MermaidDiagram from '../modules/MermaidDiagram.vue';
import TagAdder from './TagAdder.vue';

export default {
  components: {
    MarkdownPage,
    MermaidDiagram,
  },
  data() {
    return {
      resource: {
        name: 'Some resource name',
        link: 'https://github.com/MIZiper/rdb.git',
        description: 'Some long long description.',

        type: undefined,
        content: null,
      },
      dynamicComponent: null,
      requestData: '',

      AvailableModules: [
        { title: "Markdown", vueName: "MarkdownPage" },
        { title: "Mermaid Diagram", vueName: "MermaidDiagram" },
      ],
    }
  }
}

</script>