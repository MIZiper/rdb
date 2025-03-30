<template>
  <v-app>
    <v-app-bar color="secondary">
      <a href="/">
        <v-img src="./assets/logo-w.png" height="48" width="48" class="ml-4" />
      </a>
      <v-toolbar-title>Resource database</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <v-btn href="/resources/new" title="Add resource"><v-icon>mdi-plus</v-icon></v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
</script>
