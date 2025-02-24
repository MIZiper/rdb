import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import MainSearch from '../components/MainSearch.vue';
import NewPage from '../components/NewPage.vue';

// Define routes
const routes = [
    { path: '/', redirect: '/search' },
    { path: '/search', component: MainSearch, meta: { title: 'Resources List' } },
    { path: '/resources/new', component: NewPage, meta: { title: 'New Resource' } },
    { path: '/resources/:resource_id', component: MainPage, meta: { title: 'Resource Details' } },
];

// Create router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;