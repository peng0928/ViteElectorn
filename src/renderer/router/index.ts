import {createRouter, createWebHistory} from 'vue-router';
import Home from '../views/home.vue';
import ticket from '../views/orders/tickets.vue';
import login from '../views/login/index.vue';
import pendingVue from '../views/orders/pending.vue';
import pendingProVue from '../views/orders/pending-pro.vue';
import projectVue from '../views/orders/project.vue';
import ordertVue from '../views/orders/order.vue';

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
    }, {
        path: '/orders/pending/pro/:params',
        name: 'pro',
        component: pendingProVue,
    },
    {
        path: '/project/:params',
        name: 'project',
        component: projectVue,
    },
    {
        path: '/orders',
        name: 'orders',
        component: ordertVue,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;