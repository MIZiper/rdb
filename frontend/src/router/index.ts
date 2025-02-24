import { createRouter, createWebHistory } from 'vue-router';
import ContentViewerTemplate from '../components/ContentViewerTemplate.vue';
import MainPage from '../components/MainPage.vue';
import MainSearch from '../components/MainSearch.vue';
import ResourceList from '../components/ResourceList.vue';
import TagAdder from '../components/TagAdder.vue';

// Define routes
const routes = [
    { path: '/', redirect: '/search' },
    { path: '/search', component: MainSearch, meta: { title: 'Resources List' } },
    { path: '/resources/:resource_id', component: MainPage, meta: { title: 'Resource Details' } },
];

// Create router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;