import {createRouter, createWebHistory} from 'vue-router';
import Home from '../views/home.vue';
import ticket from '../views/orders/tickets.vue';
import login from '../views/login/index.vue';
import pendingVue from '../views/orders/pending.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/orders/tickets',
        name: 'tickets',
        component: ticket,
    },
    {
        path: '/login',
        name: 'login',
        component: login,
    },
    {
        path: '/orders/pending',
        name: 'pending',
        component: pendingVue,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;