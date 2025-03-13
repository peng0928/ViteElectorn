<template>
  <div class="min-h-screen">
    <a-layout class="bg-gray-100">
      <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible
        :style="{ background: 'linear-gradient(to bottom, #6366f1, #a855f7)' }" class="min-h-screen max-h-max">
        <div class="logo text-center flex items-center justify-center" @click="router.push('/')">
          <icon icon="icon-park:tickets-two" class="text-3xl hover:text-4xl duration-300 " />
        </div>
        <a-menu v-model:openKeys="state.openKeys" v-model:selectedKeys="state.selectedKeys" mode="inline"
          :inline-collapsed="state.collapsed" :items="items" :style="{ background: 'transparent' }"></a-menu>
      </a-layout-sider>
      <a-layout>
        <a-layout-header :style="{ background: '#fff', padding: 0 }">
          <div class="flex">
            <div>
              <menu-unfold-outlined v-if="collapsed" class="trigger" @click="() => (collapsed = !collapsed)" />
              <menu-fold-outlined v-else class="trigger" @click="() => (collapsed = !collapsed)" />
            </div>
            <div class="pr-5 flex gap-3 items-center  ml-auto ">
              <a-dropdown :trigger="['click']">
                <a-input-search v-model:value="state.searchValue" placeholder="搜索演唱会" enter-button="搜索" size="large"
                  @input="handleSearchInput">
                  <template #prefix>
                    <icon icon="ic:twotone-saved-search" class="text-xl" />
                  </template>
                </a-input-search>
                <template #overlay>
                  <a-menu class="w-75 line-clamp-2">
                    <div v-if="state.searchResults.length > 0">
                      <a-menu-item v-for="result in state.searchResults" :key="result.id">
                        <div class="items-center text-xs  hover:shadow-lg" @click="rPush(result.projectId)">{{
        result.name }}</div>
                      </a-menu-item>
                    </div>
                    <div v-else class="p-2 text-gray-500">
                      {{ state.isSearching ? '搜索中...' : '暂无结果' }}
                    </div>
                  </a-menu>
                </template>
              </a-dropdown>
              <div v-if="!user.nickname && !user.memberId" class="flex items-center">
                <a-button type="text" @click="router.push('/login')">
                  <div class="flex items-center gap-2 text-base">
                    <icon icon="ooui:log-in-ltr" class="align-middle" />
                    <div class=" align-middle">登录</div>
                  </div>
                </a-button>
              </div>
              <div v-else class="flex items-center">
                <a-dropdown :trigger="['click']">
                  <a-button type="text" class="h-full">
                    <div class="flex items-center justify-center gap-1 font-bold">
                      <icon icon="material-symbols:person-pin" class="align-middle" />
                      <div class="align-middle">{{ user.nickname || user.memberAuthInfoVo.realNameNonSensitive }}</div>
                    </div>
                  </a-button>
                  <template #overlay>
                    <a-menu class="line-clamp-2">
                      <a-menu-item>
                        <div class="flex items-center gap-3 text-base">
                          <icon icon="material-symbols:person-pin" class="align-middle" />
                          <div class=" align-middle">个人中心</div>
                        </div>
                      </a-menu-item>
                      <a-menu-item>
                        <div class="flex items-center gap-3 text-base" @click="logout">
                          <icon icon="ooui:log-out-ltr" class="align-middle" />
                          <div class="align-middle">退出登录</div>
                        </div>
                      </a-menu-item>
                    </a-menu>
                  </template>
                </a-dropdown>
              </div>
            </div>
          </div>
        </a-layout-header>
        <a-layout-content class="p-5">
          <div class="h-full">
            <div class="h-full">
              <router-view />
            </div>
          </div>
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script lang="ts" setup>
import { reactive, watch, h, ref, onUnmounted, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { debounce } from 'lodash-es';
import axios from 'axios';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
} from '@ant-design/icons-vue';
import router from './router';
import { Icon } from '@iconify/vue';
import { useUserStore } from './stores/userStore';
import { useRouter } from 'vue-router';

const route = useRouter()
const userStore = useUserStore();
const user = ref(userStore.userInfo);
const state = reactive({
  collapsed: false,
  selectedKeys: ['1'],
  openKeys: ['sub1'],
  preOpenKeys: ['sub1'],
  searchDropdown: ref(false),
  searchValue: ref(""),
  searchController: null as AbortController | null,
  searchResults: [] as any[],
  isSearching: false,
});
const items = reactive([
  {
    key: '1',
    icon: () => h(Icon, {
      icon: 'icon-park:music-one',
      style: { color: 'white' } // 根据需要设置颜色
    }),
    label: '演出',
    title: '演出',
    onClick: () => router.push('/') // 新增路由跳转
  },
  {
    key: '2',
    icon: () => h(Icon, {
      icon: 'ic:round-star-border-purple500',
      inline: true,
      style: { color: 'white' } // 根据需要设置颜色
    }),
    label: '订单',
    title: '订单',
    children: [
      {
        key: '3',
        label: '购票中',
        title: '购票中',
        icon: () => h(Icon, {
          icon: 'icon-park:ticket-one',
          style: { color: 'white' } // 根据需要设置颜色
        }),
        onClick: () => router.push('/orders/pending')
      },
      {
        key: '4',
        label: '票夹',
        title: '票夹',
        icon: () => h(Icon, {
          icon: 'icon-park:ticket',
          inline: true,
        }),
        onClick: () => router.push('/orders/tickets')
      },
    ],
  },
  {
    key: '5',
    icon: () => h(UserOutlined),
    label: '我的',
    title: '我的',
    onClick: () => router.push('/profile')
  },
]);
watch(
  () => state.openKeys,
  (_val, oldVal) => {
    state.preOpenKeys = oldVal;
  },
);
watch(
  () => userStore.userInfo,
  (val, oldVal) => {
    user.value = val;
  },
)
const collapsed = ref<boolean>(false);


// 创建防抖函数（500ms）
const debouncedSearch = debounce(async (value: string) => {
  try {
    state.isSearching = true;

    // 取消之前的请求
    if (state.searchController) {
      state.searchController.abort();
    }

    // 创建新控制器
    const controller = new AbortController();
    state.searchController = controller;

    const response = await axios.post('/api/search', {
      text: value
    }, {
      signal: controller.signal
    });
    console.log(response.data)
    state.searchResults = response.data.data;
    state.searchDropdown = true;
  } catch (error) {
    if (!axios.isCancel(error)) {
      console.error('搜索失败:', error);
      state.searchResults = [];
    }
  } finally {
    state.isSearching = false;
    state.searchController = null;
  }
}, 500);

// 输入处理函数
const handleSearchInput = (e: Event) => {
  const value = (e.target as HTMLInputElement).value;

  // 空值处理
  if (!value.trim()) {
    state.searchResults = [];
    state.searchDropdown = false;
    return;
  }

  debouncedSearch(value);
};

// 组件卸载时取消请求
onUnmounted(() => {
  if (state.searchController) {
    state.searchController.abort();
  }
});


const getUserInfo = async () => {
  // try {
  //   const response = await axios.post('/api/user/info');
  //   if (response.data.code === 200) {
  //     user.value = response.data.data;
  //   }
  // } catch (error) {
  //   message.error('请求异常，请检查网络');
  // }
}
const logout = async () => {
  userStore.clearUserInfo();
  user.value = {};
  // try {
  //   const response = await axios.post('/api/logout');
  //   if (response.data.code === 200) {
  //     message.success('退出成功');
  //     // 跳转到登录页
  //     router.push('/login');
  //   }
  // } catch (error) {
  //   message.error('请求异常，请检查网络');
  // }
  message.success('退出成功');
}
const rPush = (id: any) => {
  route.push({ name: 'project', params: { params: id } });
}
onMounted(() => {
  getUserInfo();
});

</script>

<style>
.trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}


.logo {
  height: 32px;
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}


/* 去掉父菜单项的文本颜色高亮 */
.ant-menu-submenu-selected>.ant-menu-submenu-title {
  color: white !important;
}


/* 添加以下样式 */
.ant-layout-sider {
  height: 100vh;
  position: fixed;
  left: 0;
  overflow: hidden;
}

.ant-layout-content {
  height: calc(100vh - 64px);
  /* 64px 是 header 高度 */
  overflow-y: auto;
}
</style>
