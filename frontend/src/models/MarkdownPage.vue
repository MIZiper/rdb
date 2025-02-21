<template>
    <div v-html="compiledMarkdown"></div>
</template>

<script>
import { marked } from 'marked';

export default {
    props: {
        data: {
            type: String,
            required: true,
        },
    },
    computed: {
        compiledMarkdown() {
            return marked(this.data);
        },
    },
}
</script>
