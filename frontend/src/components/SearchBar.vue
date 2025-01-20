<template>
  <div>
    <v-row class="ma-0" style="min-height: 40px;">
      <v-chip v-for="(tag, index) in selectedTags" :key="index" closable>
        {{ tag }}
      </v-chip>
    </v-row>
    <v-text-field ref="searchField" v-model="search" label="Add tag" @keydown.enter="addTag" @focus="onFocus"
      @input="onChange(search)" :loading="loading">
      <v-menu activator="parent" :close-on-content-click="false">
        <v-list>
          <v-list-item v-for="(tag, index) in filteredTags" :key="index" @click="selectTag(tag)">
            <v-list-item-title>{{ tag }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-text-field>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      search: '',
      childrenTags: [],
      filteredTags: [],
      selectedTags: [],
      loading: false,
      tagCache: {},
    };
  },
  methods: {
    async fetchTags(parentTag = '') {
      if (this.tagCache[parentTag]) {
        this.childrenTags = this.tagCache[parentTag];
        return;
      }
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:5428/tags/${parentTag}`);
        this.childrenTags = response.data;
        this.tagCache[parentTag] = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async onChange(val) {
      // onChange won't trigger when set this.search
      const { parent: parentTag, leaf: childTag } = this.getParentAndLeaf(val);
      await this.fetchTags(parentTag);

      if (childTag=='') { // endswith(':') or val==''
        this.filteredTags = this.childrenTags;
      } else {
        this.filteredTags = this.childrenTags.filter(tag => tag.includes(childTag));
      }
    },
    getParentAndLeaf(fullTag) {
      const parts = fullTag.split(':');
      const parent = parts.slice(0, -1).join(':');
      const leaf = parts[parts.length - 1];
      return { parent, leaf };
    },
    addTag() {
      if (this.search && !this.selectedTags.includes(this.search)) {
        this.selectedTags.push(this.search);
        this.search = '';
        this.onChange(this.search);
      }
    },
    selectTag(tag) {
      const { parent: parentTag, leaf: childTag } = this.getParentAndLeaf(this.search);
      if (parentTag) {
        this.search = `${parentTag}:${tag}`;
      } else {
        this.search = tag;
      }
      this.$nextTick(() => {
        this.$refs.searchField.focus();
      });
    },
    onFocus() {
      this.onChange(this.search);
    }
  },
  mounted() {
  },
};
</script>
