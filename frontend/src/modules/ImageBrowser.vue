<template>
    <v-file-input multiple accept="image/*" label="Select Images" v-model="pictures" prepend-icon="mdi-image" counter
        density="compact" @update:modelValue="handleFileChange"></v-file-input>
    <div class="drag-mask" :class="{ dragging: isDragging }" @dragover.prevent="showMask" @dragleave.prevent="hideMask"
        @drop.prevent="handleDrop">or drop images here</div>
    <v-row v-for="(picture, index) in pictures" :key="index">
        <v-col cols="8">
            <v-img :src="picture.preview" class="mb-2"></v-img>
        </v-col>
        <v-col cols="4">
            <v-textarea v-model="picture.remark" label="Remark" class="mb-2"></v-textarea>
        </v-col>
    </v-row>
</template>

<script>
import { apiClient } from '../config';

export default {
    data() {
        return {
            pictures: [],
            isDragging: false,
        };
    },
    methods: {
        handleFileChange(files) {
            this.pictures = Array.from(files).map(file => {
                return {
                    file,
                    preview: URL.createObjectURL(file),
                    remark: '',
                };
            });
        },
        handleDrop(event) {
            this.isDragging = false;
            const files = event.dataTransfer.files;
            const newPictures = Array.from(files).map(file => {
                return {
                    file,
                    preview: URL.createObjectURL(file),
                    remark: '',
                };
            });
            this.pictures = this.pictures.concat(newPictures);
        },
        showMask() {
            this.isDragging = true;
        },
        hideMask() {
            this.isDragging = false;
        },
        async submitPictures() {
            const formData = new FormData();
            this.pictures.forEach((picture, index) => {
                formData.append(`files[${index}]`, picture.file);
                formData.append(`remarks[${index}]`, picture.remark);
            });

            const response = await apiClient.post(`/upload`, {
                body: formData,
            });

            if (response.ok) {
                console.log('Pictures uploaded successfully');
            } else {
                console.error('Error uploading pictures');
            }
        },
    },
};
</script>

<style scoped>
.drag-mask {
    height: 60px;
    margin-bottom: 10px;
    width: 100%;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
}

.drag-mask.dragging {
    color: orange;
}
</style>
