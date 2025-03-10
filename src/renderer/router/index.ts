import {createRouter, createWebHistory} from 'vue-router';
import Home from '../views/home.vue';
import ticket from '../views/orders/tickets.vue';
import login from '../views/login/index.vue';

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
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;