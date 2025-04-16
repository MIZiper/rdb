<template>
    <template v-if="editMode">
        <!-- edit in: https://markdownlivepreview.com/ -->
        <v-textarea v-model="editData" label="Markdown Code"></v-textarea>
        <v-btn @click="compileMarkdown()" class="mb-2">Render</v-btn>
        <div v-html="editHtml"></div>
    </template>
    <div v-else v-html="compiledMarkdown"></div>
</template>

<script>
import { marked } from 'marked';

export default {
    props: {
        viewData: {
            type: String,
            required: true,
        },
        editMode: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            editData: '',
            editHtml: '',
        }
    },
    computed: {
        compiledMarkdown() {
            return marked(this.viewData);
        },
    },
    methods: {
        compileMarkdown() {
            this.editHtml = marked(this.editData);
        },
        async prepareContentForUpload() {
            return this.editData; // Return markdown content as a string
        },
    }
}
</script>
