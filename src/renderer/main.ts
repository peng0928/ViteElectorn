import {createApp} from 'vue'
import './style.css';
import '../output.css';
import App from './App.vue'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
// npx @tailwindcss/cli -i ./src/input.css -o ./src/output.css --watch
import router from './router';

import {Icon } from '@iconify/vue';

const app = createApp(App);
app.use(Antd);
app.use(router);
app.component('Icon', Icon);

app.mount('#app');
