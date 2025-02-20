<template>
  <v-card>
    <v-card-title>{{ resource.name }}</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12">
          <div class="text-subtitle-1 font-weight-medium">Tags:</div>
          <v-row class="ma-0">
            <a v-for="(tag, index) in resource.tags" :key="index" :href="`/resources?tags=${tag}`" target="_blank">
              <v-chip class="mr-1 mb-1" :color="getTagColor(tag)" variant="outlined">
                {{ tag }}
              </v-chip>
            </a>
          </v-row>
        </v-col>

        <v-col cols="12" sm="6">
          <div class="text-subtitle-1 font-weight-medium">Analysis Link:</div>
          <v-btn v-if="resource.Link2Analysis" :href="resource.Link2Analysis" variant="text" color="primary"
            prepend-icon="mdi-link" density="compact">
            View Analysis
          </v-btn>
          <div v-else class="text-body-2">No linked analysis</div>
        </v-col>

        <v-col cols="12" sm="6">
          <div class="text-subtitle-1 font-weight-medium">Last Updated:</div>
          <div class="text-body-2">
            {{ resource.UpdateDate ? new Date(resource.UpdateDate).toLocaleString() : 'Not available' }}
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { getTagColor } from './utils';

export default {
  data() {
    return {
      resource: {
        name: 'Resource Name',
        tags: ['tag1', 'tag2'],
        Link2Analysis: 'https://www.google.com',
        UpdateDate: new Date().toISOString(),
      },
    };
  },
  methods: {
    getTagColor,
  },
}
</script>
