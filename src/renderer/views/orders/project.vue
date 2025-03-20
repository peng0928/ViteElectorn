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
                <div class="flex gap-3 mt-3">
                  <div v-for="item in concert.projectServices"
                    class="text-black font-light flex items-center justify-center">
                    <div>
                      <icon :icon="item.type === 1 ? 'material-symbols:check-circle-outline' : 'codicon:error'"></icon>
                    </div>
                    <div>{{ item.title }}</div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 在线购票按钮 -->
            <div class="flex gap-3 mt-auto">
              <div
                class="w-full bg-gradient-to-r from-yellow-500 to-blue-600 text-white font-bold py-3 rounded-lg shadow-lg text-center">
                {{ concert.saleStartTime ? concert.saleStartTime : "抢先看" }}
              </div>
              <div @click="showModal"
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
  <a-modal v-model:open="open" title="" @ok="handleOk" :footer="null" :width=600>
    <div v-if="step === 1">
      <div class="text-2xl font-bold">选择场次</div>
      <div class="p-3">
        <div v-for="performInfos in data.performInfos">
          <div class=" ">
            <div v-for="(performInfo, index) in performInfos.performInfo">
              <div class="">
                <div class="inline-flex space-x-2">
                  <div v-for="item in performInfo.tags"
                    class="bg-orange-500 text-white text-xs px-2 py-1 rounded-full shadow-md">
                    <div>{{ item.tag }}</div>
                  </div>
                </div>
              </div>
              <div class="mb-5" @click="getseatPlans(performInfo.id)">
                <div
                  :class="['relative', 'inline-flex', 'p-3', 'rounded-lg', 'ring-2', 'ring-orange-500', 'cursor-pointer', { 'bg-[#ffdfe0]': isActive({ n: 1, k: performInfo.id }) }]">
                  <div class="flex gap-1 text-red-6">
                    <div class="text-base font-bold">
                      {{ performInfo.name }}
                    </div>
                    <div class="text-md mt-auto" v-if="performInfo.label">
                      ({{ performInfo.label }})
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
      <div class="text-2xl font-bold">选择票品</div>
      <div class="p-3">
        <div class="flex flex-wrap gap-6 text-nowrap">
          <div v-for="performInfo in seatPlans" :key="performInfo.id" class="flex gap-2">
            <div v-if="isIndex(performInfo.seatPlanId)" class="flex p-2">
              <div class="flex items-center justify-center">
                <div class="relative items-center justify-center w-5 h-full">
                  <img
                    :src="'/public/' + (isIndex(performInfo.seatPlanId) > 4 ? 4 : isIndex(performInfo.seatPlanId)) + '.svg'"
                    alt="状态图标" class="w-full h-full flex items-center justify-center object-cover rounded-t-md" />
                  <div class="absolute top-[40%] left-1/2 -translate-x-1/2 -translate-y-1/2 text-white font-medium">
                    {{ isIndex(performInfo.seatPlanId) }}
                  </div>
                </div>
              </div>
            </div>
            <div :class="['inline-flex', 'p-3', 'rounded-lg', 'ring-2', ' ring-orange-500', 'cursor-pointer', {
              'bg-[#ffdfe0] ring-orange-6': isActive({ n: 2, id: performInfo.seatPlanId, pid: performInfo.performId, name: performInfo.seatPlanName }),
            }]"
              @click="toggleBackground({ n: 2, id: performInfo.seatPlanId, pid: performInfo.performId, name: performInfo.seatPlanName })">
              <div class="flex gap-3 text-red-600 items-center justify-center">
                <div class="text-base font-bold">
                  {{ performInfo.seatPlanName }}
                </div>

                <div class="text-xs ring-1 ring-orange-6 rounded-lg" v-if="get_tags(performInfo.tags)">
                  <div class="p-1">{{ get_tags(performInfo.tags) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex font-bold items-center justify-center">
        <div class="flex gap-3 text-lg">
          <div>购买票数</div>
          <div class="text-gray-6 text-sm mt-auto">每人每场限购{{ data.purchaseLimitationOnce }}张</div>
        </div>
        <div class="ml-auto">
          <div class="flex gap-3 items-center justify-center">
            <div>
              <a-button type="text" shape="circle" :disabled="quantity <= 1" @click="decrease">
                <template #icon>
                  <MinusCircleFilled />
                </template>
              </a-button>
            </div>
            <div class="font-bold text-lg">{{ quantity }}</div>
            <div>
              <a-button type="text" shape="circle" @click="increase" :disabled="quantity >= data.purchaseLimitationOnce">
                <template #icon>
                  <PlusCircleFilled />
                </template>
              </a-button>
            </div>
          </div>
        </div>
      </div>
      <div @click="getMember"
        class="mt-3 hover:ring-2 hover:ring-black w-full bg-gradient-to-r from-yellow-400 to-blue-500 cursor-pointer  text-white font-bold py-3 rounded-lg shadow-lg text-center">
        下一步
      </div>
    </div>
    <div v-else>
      <icon icon="ion:md-arrow-round-back" class="text-4xl cursor-pointer" @click="step = 1" />
      <div class="text-2xl font-bold">实名持票人</div>
      <div class="text-md font-bold text-gray-6">需要选择{{ quantity }}位: 入场需要携带相关证件</div>
      <div class="p-3 grid gap-5">
        <div v-for="item in member" class="">
          <div class="items-center flex">
            <div>
              <div class="text-lg font-bold">{{ item.name }}</div>
              <div class="text-sm font-bold text-gray-6">{{ item.idCard }}</div>
            </div>
            <div class="ml-auto">
              <a-checkbox @click="checkChange(item.frequentContactsId)"
                :checked="memberChecked.includes(item.frequentContactsId)"></a-checkbox>
            </div>
          </div>
        </div>
      </div>
      <a-progress :percent="percent" :status="status" v-if="percent > 0" />
      <div>
        <div class="flex gap-5">
          <div @click="orderCreate(true)"
            class="mt-3 hover:ring-2 hover:ring-black w-full bg-gradient-to-r from-yellow-5 to-blue-6 cursor-pointer  text-white font-bold py-3 rounded-lg shadow-lg text-center">
            预约抢票
          </div>
          <div @click="orderCreate"
            class="mt-3 hover:ring-2 hover:ring-black w-full bg-gradient-to-r from-red-5 to-blue-6 cursor-pointer  text-white font-bold py-3 rounded-lg shadow-lg text-center">
            立即购买
          </div>
        </div>
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
import { PlusCircleFilled, MinusCircleFilled } from '@ant-design/icons-vue';
import { useUserStore } from '../../stores/userStore';
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const params = ref(route.params.params);
const concert = ref({ venueInfo: {} });
const isH = ref('max-h-50');
const isExpanded = ref(false);
const isOverflowing = ref(true);
const open = ref<boolean>(false);
const memberChecked = ref([]);
const step = ref(1);
const seatPlans = ref([])
const member = ref([])
const activeIndexes = ref<any[]>([]);
const data = ref({
  performInfos: []
})
const quantity = ref(1); //购票数量
const percent = ref(0);
const isRunning = ref(false);
const status = ref<'active' | 'success' | 'exception'>('active');
const startProgress = () => {
  if (isRunning.value) return;

  isRunning.value = true;
  percent.value = 0;
  status.value = 'active';
  const getRandomIncrement = () => Math.floor(Math.random() * 10) + 1;
  const interval = setInterval(() => {
    const increment = getRandomIncrement()
    if (percent.value < 90) {
      percent.value += increment;
    } else {
      clearInterval(interval!);
      isRunning.value = false;
    }
  }, 100);
};

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
const goBack = () => {
  router.back(); // 返回上一个路由
};

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
  percent.value = 0;
  getperforms()
};

const getperforms = async () => {
  const value = data.value;
  step.value = 1;
  if (value.performInfos.length <= 0) {
    try {
      const response = await axios.post('/api/performs', {
        id: params.value
      });
      if (response.data.code === 200) {
        data.value = response.data.data;
        open.value = true;
      } else {
        message.error(response.data.msg);
      }
    } catch (error) {
      message.error('请求异常，请检查网络');
    }
  } else {
    open.value = true;
  }
}

const isActive = (index: any) => {
  const hasObject = activeIndexes.value.some(item =>
    Object.keys(item).length === Object.keys(index).length &&
    Object.keys(item).every(key => item[key] === index[key])
  );
  return hasObject;
};
const isIndex = (id: any) => {
  const filteredArray = activeIndexes.value.filter(item => item.n === 2);
  const findIndex = filteredArray.findIndex(item => item.id === id);
  return findIndex + 1 || false;
}
const toggleBackground = (index: any) => {
  if (isActive(index)) {
    // 如果已经激活，则取消激活
    activeIndexes.value = activeIndexes.value.filter((i) => JSON.stringify(i) !== JSON.stringify(index));
  } else {
    activeIndexes.value.push(index);
  }
};


const increase = () => {
  quantity.value += 1;
};

const decrease = () => {
  if (quantity.value > 1) {
    quantity.value -= 1;
  }
};

const checkSeat = () => {
  const data = activeIndexes.value;
  let is_select = false;
  data.some((item: any) => {
    if (item.n === 2) {
      if (member.value.length === 0) {
        makeRequest('/api/member', member);
      } else {
        step.value = 2;
      }
      is_select = true;
      return true;
    }
  })
  if (!is_select) {
    message.warning('请选择座位');
  }
}

const getProject = async () => {
  concert.value = { venueInfo: {} };
  await makeRequest('/api/project', concert, { id: params.value });
}

const getMember = async () => {
  checkSeat()
}
const makeRequest = async (url: string, object: any, data: any = {}) => {
  try {
    const response = await axios.post(url, data);
    if (response.data.code === 200) {
      object.value = response.data.data;
      step.value = 2;
    } else {
      message.error(response.data.msg);
    }
  } catch
  (error) {
    message.error('请求异常，请检查网络');
  }
}
const checkChange = (idCard: any) => {
  if (memberChecked.value.includes(idCard)) {
    memberChecked.value = memberChecked.value.filter(item => item !== idCard);
  }
  else {
    if (quantity.value > memberChecked.value.length) {
      memberChecked.value.push(idCard)
    }
  }

};
const get_tags = (tags: any) => {
  let result = false
  tags.some(tag => {
    if (tag.type === 4) {
      result = "缺票登记"
    }
  })
  return result;
}

const ticketInfo = () => {
  const kValue = activeIndexes.value.find(item => item.n === 1)?.k;

  const idArray = activeIndexes.value
    .filter(item => item.n === 2)
    .map(item => item.id);

  return {
    k: kValue,
    ids: idArray
  };
}
const orderCreate = async (task = false) => {
  if (memberChecked.value.length === 0) {
    message.warning("请选择实名持票人")
    return
  }
  if (memberChecked.value.length != quantity.value) {
    message.warning(`请选择${quantity.value}个实名持票人`)
    return
  }
  const tinfo = ticketInfo();
  const item = concert.value;
  const userInfo = userStore.userInfo

  const query = {
    name: userInfo.memberAuthInfoVo.realNameNonSensitive,
    phnoe: userInfo.realPhone,
    deliveryType: item.deliveryType,
    projectId: item.projectId,
    performId: tinfo.k,
    audienceCount: quantity.value,
    frequentIds: memberChecked.value,
    seatPlanIds: tinfo.ids,
  }
  if (task === true) {
    const seatInfo = activeIndexes.value
      .filter(item => item.n === 2) // 筛选出 n 为 2 的对象
      .map(item => item.name)
    const ticketInfo = {
      poster: concert.value.poster,
      name: concert.value.projectName,
      startDate: concert.value.projectStartDate,
      seat: seatInfo,
      uid: userInfo.uid
    }

    try {
      const response = await axios.post('/api/task', { data: query, ...ticketInfo });
      if (response.data.code === 200) {
        message.success('成功');
      } else {
        message.error(response.data.msg);
      }
    } catch
    (error) {
      message.error('请求异常，请检查网络');
    }
  }
  else {
    startProgress()
    try {
      const response = await axios.post('/api/order/create', { ...query });
      if (response.data.code === 200) {
        percent.value = 100;
        status.value = 'success'
        message.success('成功');
      } else {
        percent.value = 100;
        status.value = 'exception'
        message.error(response.data.msg);
      }
    } catch
    (error) {
      message.error('请求异常，请检查网络');
    }
  }
}

onMounted(() => {
  getProject();
})

onBeforeRouteUpdate((to, from, next) => {
  params.value = to.params.params;
  getProject();
  member.value = [];
  data.value = {
    performInfos: []
  };
  // 在这里处理参数变化后的逻辑
  next();
});

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