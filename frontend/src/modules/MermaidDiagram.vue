<template>
    <div ref="mermaidContainer">
        <pre class="mermaid">{{ data }}</pre>
    </div>
</template>

<script>
import mermaid from 'mermaid';

export default {
    props: {
        data: {
            type: String,
            required: true,
        },
    },
    mounted() {
        mermaid.initialize({ startOnLoad: true });
    },
    methods: {
        renderDiagram() { // didn't run with startOnLoad=True
            mermaid.run();
        },
    },
}
</script>
