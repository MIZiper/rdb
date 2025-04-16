<template>
    <template v-if="editMode">
        <!-- edit in: https://mermaid.live/ -->
        <v-textarea v-model="editData" label="Mermaid Code"></v-textarea>
        <v-btn @click="renderDiagram()" class="mb-2">Render</v-btn>
        <div id="editContainer"></div>
    </template>
    <div v-else ref="mermaidContainer">
        <pre class="mermaid">{{ viewData }}</pre>
    </div>
</template>

<script>
import mermaid from 'mermaid';

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
        }
    },
    mounted() {
        mermaid.initialize();
        this.$nextTick(() => {mermaid.run()});
    },
    methods: {
        renderDiagram() {
            const editContainer = document.getElementById("editContainer");
            editContainer.innerHTML = "";
            const preNode = document.createElement("pre");
            preNode.className = "mermaid";
            preNode.textContent = this.editData;
            editContainer.appendChild(preNode);
            mermaid.run();
        },
        async prepareContentForUpload() {
            return this.editData; // Return diagram content as a string
        },
    },
}
</script>
