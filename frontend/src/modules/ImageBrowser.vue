<template>
    <template v-if="editMode">
        <v-file-input multiple accept="image/*" label="Select Images" v-model="pictures" prepend-icon="mdi-image"
            counter density="compact" @update:modelValue="handleFileChange"></v-file-input>
        <div class="drag-mask" :class="{ dragging: isDragging }" @dragover.prevent="showMask"
            @dragleave.prevent="hideMask" @drop.prevent="handleDrop">or drop images here</div>
        <v-row v-for="(picture, index) in pictures" :key="index">
            <v-col cols="8">
                <v-img :src="picture.preview" class="mb-2"></v-img>
            </v-col>
            <v-col cols="4">
                <v-textarea v-model="picture.remark" label="Remark" class="mb-2"></v-textarea>
            </v-col>
        </v-row>
    </template>
    <template v-else>
        <v-row v-for="(picture, index) in pictures" :key="index">
            <v-card class="mb-2">
                <v-img :src="picture.preview"></v-img>
                <v-card-title>{{ picture.remark }}</v-card-title>
            </v-card>
        </v-row>
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
    },
    data() {
        return {
            pictures: [],
            isDragging: false,
        };
    },
    mounted() {
        if (this.data) {
            const parsedData = JSON.parse(this.data);
            this.pictures = parsedData.map(item => ({
                file: item.file,
                preview: URL.createObjectURL(item.file),
                remark: item.remark,
            }));
        }
    },
    methods: {
        handleFileChange(files) {
            const MAX_DIMENSION = 1024; // Limit max height or width to 1024px
            this.pictures = [];

            Array.from(files).forEach(file => {
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
                            this.pictures.push({
                                file: resizedFile,
                                preview: URL.createObjectURL(resizedFile),
                                remark: '',
                            });
                        }, file.type);
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
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
        async prepareContentForUpload() {
            const formData = new FormData();
            this.pictures.forEach((picture, index) => {
                formData.append(`files[${index}]`, picture.file);
                formData.append(`remarks[${index}]`, picture.remark);
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
