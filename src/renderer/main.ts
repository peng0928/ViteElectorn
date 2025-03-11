import {createApp} from 'vue'
import './style.css';
import App from './App.vue'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
// npx @tailwindcss/cli -i ./src/input.css -o ./src/output.css --watch
import router from './router';

import {Icon} from '@iconify/vue';
import {createPinia} from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(Antd);
app.use(router);
app.use(pinia);
app.component('Icon', Icon);

app.mount('#app');
