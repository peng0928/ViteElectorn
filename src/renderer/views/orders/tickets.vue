<template>
  <div class="p-5 pb-15">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h2 class="font-bold text-2xl text-gray-800">我的票夹</h2>
    </div>

    <!-- 票夹列表 -->
    <div class="grid gap-6 xl:grid-cols-2 2xl:grid-cols-4 lg:grid-cols-2 md:grid-cols-1 sm:grid-cols-1 xs:grid-cols-1"
      v-if="ticketShop.length > 0">
      <div v-for="(item, index) in ticketShop ">
        <div
          class="relative h-64 w-[95%] p-4 rounded-2xl transition-transform hover:scale-105 duration-300 bg-gradient-to-r from-blue-600/50 to-purple-600/50 hover:from-blue-700/60 hover:to-purple-700/60 shadow-lg">
          <!-- 票面内容 -->
          <div class="flex h-full w-full">
            <div class="h-full w-38">
              <img :src="item.poster" class="w-full h-[80%] rounded-2xl object-cover" alt="演唱会图片" />
            </div>
            <div class="ml-3 p-2 w-2/3">
              <h3 class="text-md font-bold text-gray-800 line-clamp-2">
                {{ item.projectName }}
              </h3>
              <div class="text-gray-600 mt-2 text-sm ">
                <div class="line-clamp-1">{{ item.venueInfo.city }} | {{ item.venueInfo.name }}</div>
                <div class="line-clamp-1">{{ item.performStartTime }}</div>
              </div>
              <div class="mt-15 flex gap-2">
                <div class="bg-[#ff5e63] rounded-md text-white w-12 font-bold text-center">
                  <div class="p-1">{{ item.ticketCount }}张票</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 虚线分割线 -->
          <div class="absolute left-0 w-full top-[80%] border-b-2 border-dotted border-[#f1a15a]"></div>

          <!-- 左侧缺口 -->
          <div class="absolute top-[81%] -left-2 w-4 h-4 bg-[#f5f5f5] -translate-y-1/2 rounded-2xl"></div>

          <!-- 右侧缺口 -->
          <div class="absolute top-[81%] -right-2 w-4 h-4 bg-[#f5f5f5] -translate-y-1/2 rounded-2xl"></div>

          <!-- 状态图标 -->
          <div class="absolute top-[73%] w-4 h-4 right-15 -translate-y-1/2 rounded-2xl">
            <img src="/utils/img/end.svg" alt="状态图标" v-if="isDateGreaterThanToday(item.performStartTime)" />
            <img src="/utils/img/qd.svg" alt="状态图标" v-else />
          </div>

          <!-- 底部提示 -->
          <div class="absolute top-[88%]">
            <div class="text-nowrap text-gray-600">请携带身份证原价直刷进场</div>
          </div>

        </div>
      </div>
    </div>
    <div v-else class="rounded-2xl h-75 w-full overflow-hidden">
      <!-- 科技感骨架屏 -->
      <div class="h-full w-full animate-gradient-x">
        <a-skeleton active :paragraph="{ rows: 8 }" class="rounded-2xl bg-opacity-0">
          <a-skeleton-image class="w-full h-full rounded-2xl bg-opacity-0" />
        </a-skeleton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { message } from 'ant-design-vue';
import axios from 'axios';
import { reactive, watch, h, ref, onUnmounted, onMounted } from 'vue';
import { useUserStore } from '../../stores/userStore';

const userStore = useUserStore();

const ticketShop = ref(
  []
)

const getTicket = async () => {
  try {
    const response = await axios.post('/api/ticket', {});
    if (response.data.code === 200) {
      ticketShop.value = response.data.data;
    }
    else {
      message.error(response.data.msg);
      userStore.clearUserInfo();
    }
  } catch (error) {
    message.error('请求异常，请检查网络');
  }
}
const isDateGreaterThanToday = (dateString: string) => {
  const standardizedDateString = dateString.replace(/\//g, '-');
  const inputDate = new Date(standardizedDateString);
  // 获取当前时间
  const today = new Date();
  // 比较日期
  return inputDate < today;
}

onMounted(() => {
  getTicket()
})
</script>

<style scoped>
svg path {
  fill: #008095;
}

.border-indigo-600 {
  border-color: transparent !important;
  /* 这会覆盖 Tailwind CSS 的样式 */
}
</style>