<template>
    <template v-if="editMode">
        <v-file-input ref="fileInput" multiple accept="image/*" label="Select Images" prepend-icon="mdi-image" counter
            chips show-size density="compact" @update:modelValue="handleFileChange"></v-file-input>
        <div class="drag-mask" :class="{ dragging: isDragging }" @dragover.prevent="showMask"
            @dragleave.prevent="hideMask" @drop.prevent="handleDrop">or drop images here (appending)</div>
        <v-row v-for="(picture, index) in pictures" :key="index">
            <v-col cols="8">
                <small>{{ picture.file.name }}</small>
                <v-img :src="picture.url" class="mb-2"></v-img>
            </v-col>
            <v-col cols="4">
                <v-textarea v-model="picture.remark" label="Remark" class="mb-2"></v-textarea>
            </v-col>
        </v-row>
    </template>
    <template v-else>
        <template v-for="(picture, index) in pictures" :key="index">
            <v-img :src="picture.url"></v-img>
            <p class="pa-1">{{ picture.remark }}</p>
            <hr class="mt-2 mb-2" />
        </template>
    </template>
</template>

<script>
export default {
    props: {
        viewData: {
            type: Array,
            required: true,
        },
        editMode: {
            type: Boolean,
            default: false,
        },
        resizeImages: {
            type: Boolean,
            default: true, // Enable resizing by default
        },
    },
    data() {
        return {
            pictures: [], // {file, url, remark}
            isDragging: false,
        };
    },
    mounted() {
        if (this.viewData) {
            this.pictures = this.viewData.map(item => ({
                file: null,
                url: item.url,
                remark: item.remark,
            }));
        }
    },
    methods: {
        async resizeImageAndUrl(file) {
            const MAX_DIMENSION = 1024; // Limit max height or width to 1024px
            return new Promise(resolve => {
                if (!this.resizeImages) {
                    // Skip resizing if resizeImages is false
                    resolve({
                        file,
                        url: URL.createObjectURL(file),
                        remark: '',
                    });
                    return;
                }

                const reader = new FileReader();
                reader.onload = event => {
                    const img = new Image();
                    img.onload = () => {
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');

                        let width = img.width;
                        let height = img.height;

                        if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
                            if (width > height) {
                                height *= MAX_DIMENSION / width;
                                width = MAX_DIMENSION;
                            } else {
                                width *= MAX_DIMENSION / height;
                                height = MAX_DIMENSION;
                            }
                        }

                        canvas.width = width;
                        canvas.height = height;
                        ctx.drawImage(img, 0, 0, width, height);

                        canvas.toBlob(blob => {
                            const resizedFile = new File([blob], file.name, { type: file.type });
                            resolve({
                                file: resizedFile,
                                url: URL.createObjectURL(resizedFile),
                                remark: '',
                            });
                        }, file.type);
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
            });
        },
        async handleFileChange(files) {
            this.pictures = [];
            for (const file of files) {
                const picture = await this.resizeImageAndUrl(file);
                this.pictures.push(picture);
            }
        },
        async handleDrop(event) {
            this.isDragging = false;
            const files = event.dataTransfer.files;
            for (const file of files) {
                const picture = await this.resizeImageAndUrl(file);
                this.pictures.push(picture);
                this.$refs.fileInput.modelValue.push(file); // will not trigger `handleFileChange`
            }
        },
        showMask() {
            this.isDragging = true;
        },
        hideMask() {
            this.isDragging = false;
        },
        async prepareContentForUpload() {
            const formData = new FormData();
            this.pictures.forEach((picture, index) => {
                formData.append(`files[]`, picture.file);
                formData.append(`remarks[]`, picture.remark);
            });
            return formData; // Return images and remarks as FormData
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
