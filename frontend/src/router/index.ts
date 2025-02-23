
import { createRouter, createWebHistory } from 'vue-router';
import ContentViewerTemplate from '../components/ContentViewerTemplate.vue';
import MainPage from '../components/MainPage.vue';
import MainSearch from '../components/MainSearch.vue';
import ResourceList from '../components/ResourceList.vue';
import TagAdder from '../components/TagAdder.vue';

// Define routes
const routes = [
    { path: '/', redirect: '/resources' },
    { path: '/resources', component: MainSearch },
    { path: '/resources/:resource_id', component: MainPage },
];

// Create router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;