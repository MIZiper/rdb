<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-select label="Resource Types" v-model="dynamicComponent" :items="AvailableModules" item-title="title" item-value="vueName"></v-select>
        <component v-if="dynamicComponent" :editMode="true" :is="dynamicComponent" ref="component"></component>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>New Resource</v-card-title>
          <v-card-text>
            <v-text-field density="compact" v-model="resource.title" label="Title"></v-text-field>
            <v-text-field density="compact" v-model="resource.link" label="Link"></v-text-field>
            <v-textarea density="compact" v-model="resource.description" label="Description"></v-textarea>

            <v-divider />
            <div class="text-subtitle-1 font-weight-medium">Tags:</div>
            <TagAdder ref="tagAdder" />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" variant="outlined" @click="submitResource">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MarkdownPage from '../modules/MarkdownPage.vue';
import MermaidDiagram from '../modules/MermaidDiagram.vue';
import ImageBrowser from '../modules/ImageBrowser.vue';
import TagAdder from './TagAdder.vue';
import { apiClient, TAG_SPLITTER } from '../config';

export default {
  components: {
    MarkdownPage,
    MermaidDiagram,
    ImageBrowser,
  },
  data() {
    return {
      resource: {
        title: '',
        link: 'https://github.com/MIZiper/rdb.git',
        description: '',
        tags: '',

        module: undefined,
        content: null,
      },
      dynamicComponent: null,

      AvailableModules: [
        { title: "Markdown", vueName: "MarkdownPage" },
        { title: "Mermaid Diagram", vueName: "MermaidDiagram" },
        { title: "Image Browser", vueName: "ImageBrowser" },
      ],
    }
  },
  methods: {
    async submitResource() {
      // validate resource
      if (this.dynamicComponent != null) {
        this.resource.module = this.dynamicComponent;
        this.resource.content = this.$refs.component.editData;
      }
      this.resource.tags = this.$refs.tagAdder.selectedTags.join(TAG_SPLITTER);

      try {
        const response = await apiClient.post('/resources', this.resource);
        if (response.status === 200) {
          console.log('Resource created successfully');
        }
      } catch (error) {
        console.error('Error creating resource', error);
      }
    },
  },
}
</script>