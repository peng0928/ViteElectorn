// src/stores/userStore.ts
import {defineStore} from 'pinia';
import {ref} from 'vue';

export const useUserStore = defineStore('user', () => {
    const userInfo = ref<{}>({});

    const setUserInfo = (info: any) => {
        userInfo.value = info;
    };

    const clearUserInfo = () => {
        userInfo.value = {};
    };

    return {
        userInfo,
        setUserInfo,
        clearUserInfo,
    };
}, {
    persist: true, // 启用持久化
});