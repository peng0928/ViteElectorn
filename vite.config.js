const Path = require('path');
const vuePlugin = require('@vitejs/plugin-vue')


const {defineConfig} = require('vite');

/**
 * https://vitejs.dev/config
 */
const config = defineConfig({
    root: Path.join(__dirname, 'src', 'renderer'),
    publicDir: 'public',
    server: {
        port: 8080,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:6688', // 你的后端地址
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '/api')
            }
        }
    },
    open: false,
    build: {
        outDir: Path.join(__dirname, 'build', 'renderer'),
        emptyOutDir: true,
    },
    plugins: [
        vuePlugin(),
    ],
});

module.exports = config;
