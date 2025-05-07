<template>
    <pre>{{ viewData }}</pre>
</template>

<script>
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
}
</script>

<style>
pre {
    white-space: pre-wrap;       /* Since CSS 2.1 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}
</style>
