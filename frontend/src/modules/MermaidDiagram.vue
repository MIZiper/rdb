<template>
    <template v-if="editMode">
        <!-- edit in: https://mermaid.live/ -->
        <v-textarea v-model="editData" label="Mermaid Code"></v-textarea>
        <v-btn @click="renderDiagram()" class="mb-2">Render</v-btn>
        <div id="editContainer"></div>
    </template>
    <div v-else ref="mermaidContainer">
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
        mermaid.initialize({ startOnLoad: true });
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
    },
}
</script>
