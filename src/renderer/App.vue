<template>
  <div class="h-screen">
    <a-layout class="h-full">
      <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible
                      :style="{ background: 'linear-gradient(to bottom, #6366f1, #a855f7)' }">
        <div class="logo text-center flex items-center justify-center h-full">
          <icon icon="icon-park:tickets-one" class="text-3xl hover:text-4xl duration-300 "/>
        </div>
        <a-menu
            v-model:openKeys="state.openKeys"
            v-model:selectedKeys="state.selectedKeys"
            mode="inline"
            :inline-collapsed="state.collapsed"
            :items="items"
            :style="{ background: 'transparent'}"
        ></a-menu>
      </a-layout-sider>
      <a-layout>
        <a-layout-header style="background: #fff; padding: 0">
          <div class="flex justify-between">
            <div>
              <menu-unfold-outlined
                  v-if="collapsed"
                  class="trigger"
                  @click="() => (collapsed = !collapsed)"
              />
              <menu-fold-outlined v-else class="trigger" @click="() => (collapsed = !collapsed)"/>
            </div>
            <div class="pr-5">
              <a-dropdown :trigger="['click']">
                <a-button type="text">
                  <template #icon>
                    <icon icon="icon-park:tickets-one" />
                  </template>
                    登录
                </a-button>
                <template #overlay>
                  <a-menu>
                    <a-menu-item key="3">3rd menu item</a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </div>
          </div>

        </a-layout-header>
        <a-layout-content :style="{background: '#fff' }" class="p-5">
          <div>
            <router-view/>
          </div>
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>
<script lang="ts" setup>
import {reactive, watch, h, ref} from 'vue';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  MailOutlined,
  CustomerServiceOutlined,
} from '@ant-design/icons-vue';

const state = reactive({
  collapsed: false,
  selectedKeys: ['1'],
  openKeys: ['sub1'],
  preOpenKeys: ['sub1'],
});
const items = reactive([
  {
    key: '1',
    icon: () => h(CustomerServiceOutlined),
    label: '演出',
    title: '演出',
  },
  {
    key: 'sub1',
    icon: () => h(MailOutlined),
    label: 'Navigation One',
    title: 'Navigation One',
    children: [
      {
        key: '5',
        label: 'Option 5',
        title: 'Option 5',
      },
    ],
  },
]);
watch(
    () => state.openKeys,
    (_val, oldVal) => {
      state.preOpenKeys = oldVal;
    },
);
const collapsed = ref<boolean>(false);
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
.ant-menu-submenu-selected > .ant-menu-submenu-title {
  color: white !important;
}


</style>
