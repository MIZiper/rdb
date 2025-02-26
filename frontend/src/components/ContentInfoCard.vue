<template>
  <v-card>
    <v-card-title>{{ resource.name }}</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12">
          <div class="text-subtitle-1 font-weight-medium">Tags:</div>
          <v-row class="ma-0">
            <a v-for="(tag, index) in resource.tags" :key="index" :href="`/search?tags=${tag}`">
              <v-chip class="mr-1 mb-1" :color="getTagColor(tag)" variant="outlined">
                {{ tag }}
              </v-chip>
            </a>
          </v-row>
        </v-col>

        <v-col v-if="resource.description" cols="12">
          <div class="text-subtitle-1 font-weight-medium">Description:</div>
          <div class="text-body-2">
            {{ resource.description }}
          </div>
        </v-col>

        <v-col cols="12" sm="6">
          <div class="text-subtitle-1 font-weight-medium">Analysis Link:</div>
          <v-btn v-if="resource.link" :href="resource.link" variant="text" color="primary"
            prepend-icon="mdi-link" density="compact">
            View Analysis
          </v-btn>
          <div v-else class="text-body-2">[No linked analysis]</div>
        </v-col>

        <v-col cols="12" sm="6">
          <div class="text-subtitle-1 font-weight-medium">Last Updated:</div>
          <div class="text-body-2">
            {{ resource.update_date ? new Date(resource.update_date).toLocaleString() : '[Not available]' }}
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { getTagColor } from './utils';

export default {
  props: {
    resource: {
      type: Object,
      required: true,
    },
  },
  methods: {
    getTagColor,
  },
}
</script>
