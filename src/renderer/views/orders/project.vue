<template>
  <div class="relative">
    <div class="fixed w-full">
      <icon icon="ion:md-arrow-round-back" class="text-4xl cursor-pointer" @click="goBack()" />
    </div>
  </div>
  <div class="rounded-2xl mx-auto w-[85%] pb-10">
    <div class="">
      <div class="p-5 rounded-lg shadow-2xl">
        <div class="flex gap-5 h-90 ">
          <!-- 演出海报 -->
          <div class="relative overflow-hidden rounded-lg shadow-2xl w-1/4 min-w-64 max-w-75">
            <img :src="concert.poster" alt=""
              class="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500" />
            <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
            <div class="absolute bottom-8 left-6 w-[80%] transform duration-500 hover:-translate-y-2">
              <h1 class="text-md font-bold text-white line-clamp-2">{{ concert.projectName }}</h1>
              <p class="text-lg text-gray-300">{{ concert.projectStartDate }}</p>
            </div>
          </div>
          <!-- 演出信息 -->
          <div class=" text-black flex flex-col h-full w-[80%]">
            <div class="text-xl font-bold">{{ concert.projectName }}</div>
            <div class="text-lg text-red-5 font-semibold">
              ¥ {{ concert.lowPrice }}~{{ concert.highPrice }}
            </div>
            <div class="p-2">
              <div class="text-md font-semibold text-gray-6">
                <div class="flex gap-1">
                  <div>场馆:</div>
                  <div class="">
                    <div>{{ concert.venueInfo.city }}|{{ concert.venueInfo.name }}</div>
                    <div class="text-sm">{{ concert.venueInfo.address }}</div>
                  </div>
                </div>
                <div class="flex gap-1">
                  <div>时间:</div>
                  <div class="">{{ concert.timeDisplay }}</div>
                </div>

              </div>
            </div>
            <!-- 在线购票按钮 -->
            <div class="flex gap-3 mt-auto">
              <div @click="showModal"
                class="hover:ring-2 hover:ring-black w-full bg-gradient-to-r from-yellow-500 to-blue-600 cursor-pointer text-white font-bold py-3 rounded-lg shadow-lg text-center">
                预定
              </div>
              <div
                class="hover:ring-2 hover:ring-black w-full bg-gradient-to-r from-red-500 to-blue-600 cursor-pointer  text-white font-bold py-3 rounded-lg shadow-lg text-center">
                立即购票
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="p-5 rounded-lg shadow-2xl">
        <div :class="['overflow-auto scrollbar-hide', isH]" v-html="concert.details"></div>
        <div v-if="isOverflowing" class="mt-2 text-center cursor-grabbing">
          <div @click="toggleExpand" class="text-blue-500 hover:text-blue-700">
            {{ isExpanded ? '收起' : '展开' }}
          </div>
        </div>
      </div>
    </div>
  </div>
  <a-modal v-model:open="open" title="" @ok="handleOk" :footer="null">
    <div>
      <div class="text-2xl font-bold">选择场次</div>
      <div class="p-3">
        <div v-for="performInfos in data.performInfos">
          <div class=" ">
            <div v-for="(performInfo, index) in performInfos.performInfo">
              <div class="mb-5" @click="getseatPlans(performInfo.id)">
                <div
                  :class="['relative', 'inline-flex', 'p-3', 'rounded-lg', 'ring-2', 'ring-orange-500', 'cursor-pointer', 'hover:bg-[#ffdfe0]', { 'bg-[#ffdfe0]': isActive({ n: 1, k: performInfo.id }) }]">
                  <div class="flex gap-1 text-red-6">
                    <div class="text-base font-bold">
                      {{ performInfo.name }}
                    </div>
                    <div class="text-md mt-auto" v-if="performInfo.label">
                      ({{ performInfo.label }})
                    </div>
                  </div>
                  <div
                    class="absolute -right-2 -top-2 bg-orange-500 text-white text-xs px-2 py-1 rounded-full shadow-md"
                    v-if="performInfo.tags.lenght > 0">
                    {{ performInfo.tags[0].tag }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="text-2xl font-bold">选择票品</div>
      <div class="p-3">
        <div class="grid grid-cols-4 gap-5 text-nowrap">
          <div v-for="performInfo in seatPlans" :key="performInfo.id"
            :class="{ 'col-span-full': performInfo.display === 3 && performInfo.type === 3 }">
            <div
              :class="['relative', 'inline-flex', 'p-3', 'rounded-lg', 'ring-2', 'ring-orange-500', 'cursor-pointer', 'hover:bg-[#ffdfe0]', { 'bg-[#ffdfe0]': isActive({ n: 2, id: performInfo.seatPlanId, pid: performInfo.performId }) }]"
              @click="toggleBackground({ n: 2, id: performInfo.seatPlanId, pid: performInfo.performId })">
              <div class="flex gap-1 text-red-600">
                <div class="text-base font-bold">
                  {{ performInfo.seatPlanName }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div @click="handleConfirm"
        class="mt-3 hover:ring-2 hover:ring-black w-full bg-gradient-to-r from-red-500 to-blue-600 cursor-pointer  text-white font-bold py-3 rounded-lg shadow-lg text-center">
        确认
      </div>
    </div>
  </a-modal>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router';
import axios from "axios";
import { message } from "ant-design-vue";
import { Icon } from "@iconify/vue";

const route = useRoute();
const router = useRouter();
const params = ref(route.params.params);
const concert = ref({ venueInfo: {} });
const isH = ref('max-h-50');
const isExpanded = ref(false);
const isOverflowing = ref(true);
const open = ref<boolean>(false);


const handleOk = (e: MouseEvent) => {
  open.value = false;
};
const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
  if (isExpanded.value) {
    isH.value = 'max-h-auto'
  } else {
    isH.value = 'max-h-50'
  }
};
const getProject = async () => {
  concert.value = { venueInfo: {} };
  try {
    const response = await axios.post('/api/project', { id: params.value });
    if (response.data.code === 200) {
      concert.value = response.data.data;
    } else {
      message.error(response.data.msg);
    }
  } catch (error) {
    message.error('请求异常，请检查网络');
  }
}
const goBack = () => {
  router.back(); // 返回上一个路由
};
onMounted(() => {
  getProject();
})
onBeforeRouteUpdate((to, from, next) => {
  params.value = to.params.params;
  getProject();
  // 在这里处理参数变化后的逻辑
  next();
});


// 模拟数据
const data = ref({
  performInfos: []
})
const seatPlans = ref([])
const getseatPlans = (id: any) => {
  const res = { n: 1, k: id }
  if (isActive(res)) {
    // 如果已经激活，则取消激活
    activeIndexes.value = activeIndexes.value.filter((i) => JSON.stringify(i) !== JSON.stringify(res));
  } else {
    // 否则激活
    activeIndexes.value = [];
    activeIndexes.value.push(res);
  }
  console.log(activeIndexes.value)
  seatPlans.value = []
  const performInfos = data.value.performInfos;
  performInfos.forEach((item: any) => {
    const performInfo = item.performInfo;
    performInfo.forEach((info: any) => {
      const infoId = info.id;
      if (infoId === id) {
        seatPlans.value = info.seatPlans;
      }
    })
  })
}
const handleConfirm = () => {
  if (seatPlans.value.length > 0) {
    message.success('购票成功！')
    open.value = false;
    // 这里可以添加购票逻辑
  }
}

const showModal = () => {
  getperforms()
};
const getperforms = async () => {
  const value = data.value;
  if (value.performInfos.length <= 0) {
    try {
      const response = await axios.post('/api/performs', {
        id: params.value
      });
      if (response.data.code === 200) {
        data.value = response.data.data;
        open.value = true;
      }
      else {
        message.error(response.data.msg);
      }
    } catch (error) {
      message.error('请求异常，请检查网络');
    }
  }
  else {
    open.value = true;
  }
}
const activeIndexes = ref<any[]>([]);

// 判断某个索引是否处于激活状态
const isActive = (index: any) => {
  const hasObject = activeIndexes.value.some(item =>
    Object.keys(item).length === Object.keys(index).length &&
    Object.keys(item).every(key => item[key] === index[key])
  );
  return hasObject;
};
const toggleBackground = (index: any) => {
  if (isActive(index)) {
    // 如果已经激活，则取消激活
    activeIndexes.value = activeIndexes.value.filter((i) => JSON.stringify(i) !== JSON.stringify(index));

  } else {
    // 否则激活
    activeIndexes.value.push(index);
  }
};
</script>

<style scoped>
/* 自定义样式 */

.scrollbar-hide::-webkit-scrollbar {
  display: none;
  /* Chrome/Safari/Edge */
}

.scrollbar-hide {
  -ms-overflow-style: none;
  /* IE/Edge */
  scrollbar-width: none;
  /* Firefox */
}
</style>