<template>
  <v-card class="ma-4 pa-4">
    <v-card-title>{{ resource.name }}</v-card-title>
    
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <div class="text-subtitle-1 font-weight-medium">Tags:</div>
          <v-chip-group>
            <v-chip
              v-for="tag in resource.tags"
              :key="tag"
              color="primary"
              variant="outlined"
              class="ma-1"
            >
              {{ tag }}
            </v-chip>
          </v-chip-group>
        </v-col>

        <v-col cols="12" sm="6">
          <div class="text-subtitle-1 font-weight-medium">Analysis Link:</div>
          <v-btn
            v-if="resource.Link2Analysis"
            :href="resource.Link2Analysis"
            variant="text"
            color="primary"
            prepend-icon="mdi-link"
          >
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
export default {
  name: 'ContentTemplate',
  props: {
    resource: {
      type: Object,
      required: true,
      validator: (obj) => {
        return obj.hasOwnProperty('name') && 
               obj.hasOwnProperty('tags') &&
               Array.isArray(obj.tags)
      }
    }
  }
}
</script>
