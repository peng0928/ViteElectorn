<template>
  <div class="p-5 pb-15">
    <!-- 页面标题 -->
    <div class="mb-1">
      <h2 class="font-bold text-2xl text-gray-800">我的订单</h2>
    </div>

    <!-- 筛选条件 -->
    <div class="mb-1 flex space-x-4">
      <button v-for="option in filterOptions" :key="option.value" @click="filterFilter(option)" :class="[
                'px-6 py-2 rounded-lg border-2 transition-all duration-300',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                filterStatus === String(option.value)
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white border-transparent shadow-lg hover:shadow-xl'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 hover:border-blue-300',
            ]">
        <div class="flex items-center align-middle leading-none gap-1">
          <div>
            <icon :icon="option.icon" class="text-md"/>
          </div>
          <div>{{ option.label }}</div>
        </div>
      </button>
    </div>

    <div
        class="p-5 grid gap-12 custom-grid @3xl:grid-cols-4 2xl:grid-cols-3 xl:grid-cols-2 lg:grid-cols-2 md:grid-cols-1 sm:grid-cols-1 xs:grid-cols-1 h-[calc(100vh-280px)] overflow-y-auto scrollbar-hide rounded-2xl">
      <div v-for="(order, index) in paginatedOrders" :key="order.id" :class="[
        'relative h-64 w-96 p-5 rounded-lg transition-all duration-300',
        ' hover:scale-101 hover:shadow-2xl rounded-2xl',
        getCardBackground(order.orderStatus),
    ]">
        <!-- 索引标签 -->
        <div
            class="absolute -top-3 -left-3 w-8 h-8 flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold text-lg rounded-full shadow-lg glow">
          {{ index + 1 }}
        </div>
        <!-- 票面内容 -->
        <div class="flex h-full w-full">
          <div class="h-full w-38">
            <img :src="order.poster" class="w-full h-full rounded-lg" alt="演唱会图片"/>
          </div>
          <div class="ml-3 p-2 w-2/3 flex flex-col">
            <h3 class="text-md font-bold text-gray-800 line-clamp-2">{{ order.projectName }}</h3>
            <div class="text-gray-600 mt-2 font-medium text-sm">
              <div>{{ order.performStartTime }}</div>
              <div>{{ order.projectCity }} | {{ order.venueName }}</div>
            </div>
            <div class="text-sm font-medium text-black">￥{{ order.price }}/共{{ order.ticketQuantity }}张</div>
            <div class="mt-auto text-right">
              <a-tag :color="getStatusColor(order.orderStatus)">
                <template #icon>
                  <div class="flex items-center align-middle gap-1">
                    <icon :icon="getStatusIcon(order.orderStatus)" class="text-md"/>
                    <div>{{ getText(order.orderStatus) }}</div>
                  </div>
                </template>
              </a-tag>
              <a-tag :color="getStatusColor(order.orderStatus)">
                <template #icon>
                  <div class="flex items-center align-middle gap-1">
                    <div>订单时间: {{ (order.orderDate) }}</div>
                  </div>
                </template>
              </a-tag>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- 分页 -->
    <div class="mt-6 flex justify-center">
      <a-pagination v-model:current="currentPage" v-model:pageSize="pageSize" :total="total"
                    :pageSizeOptions="['5', '10', '20', '50']" show-less-items show-size-changer
                    @showSizeChange="handlePageChange" @change="handlePageChange"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {message} from 'ant-design-vue';
import axios from 'axios';
import {ref, computed, onMounted} from 'vue';

// 订单数据
const orders = ref([]);

// 筛选状态
const filterStatus = ref('all');


const filterOptions = [
  {value: 'all', type: 0, label: '全部', icon: 'ri:list-unordered'},
  {value: [200], type: 0, label: '完成', icon: 'material-symbols:check'},
  {value: [100], type: 1, label: '待支付', icon: 'icon-park-solid:flash-payment'},
  {value: [400, 300], type: 2, label: '取消/退款', icon: 'material-symbols-light:cancel'},
];

// 分页相关
// 分页相关
const currentPage = ref(1);
const pageSize = ref(5);
const total = ref(0);
const orderType = ref(0);

// 分页后的订单数据
const paginatedOrders = computed(() => {
  return filteredOrders.value;
});

const filterFilter = (filter: string) => {
  filterStatus.value = String(filter.value);
  orderType.value = filter.type;
  getOrders();
};
// 处理分页变化
const handlePageChange = (page: number, size: number) => {
  currentPage.value = page;
  pageSize.value = size;
  getOrders();
};
// 根据筛选状态过滤订单
const filteredOrders = computed(() => {
  if (filterStatus.value === 'all') {
    return orders.value;
  }
  const data = orders.value.filter(order => filterStatus.value.includes(order.orderStatus));
  console.log(filterStatus.value)
  return data;
});


// 获取状态标签颜色
const getStatusColor = (status: any) => {
  switch (status) {
    case 100:
      return 'blue';
    case 200:
      return 'green';
    case 300:
      return 'red';
    case 400:
      return 'red';
    default:
      return 'gray';
  }
};

// 获取状态图标
const getStatusIcon = (status: any) => {
  switch (status) {
    case 100:
      return 'line-md:loading-twotone-loop';
    case 200:
      return 'material-symbols:check';
    case 300:
      return 'icon-park-outline:error';
    case 400:
      return 'icon-park-outline:error';
    default:
      return 'ri:list-unordered';
  }
};

// 获取卡片背景
const getCardBackground = (status: any) => {
  switch (status) {
    case 100:
      return 'bg-gradient-to-r from-blue-500/10 to-purple-500/10 hover:from-blue-500/20 hover:to-purple-500/20';
    case 200:
      return 'bg-gradient-to-r from-green-500/10 to-teal-500/10 hover:from-green-500/20 hover:to-teal-500/20';
    case 300:
      return 'bg-gradient-to-r from-red-500/10 to-pink-500/10 hover:from-red-500/20 hover:to-pink-500/20';
    case 400:
      return 'bg-gradient-to-r from-red-500/10 to-pink-500/10 hover:from-red-500/20 hover:to-pink-500/20';
    default:
      return 'bg-gradient-to-r from-gray-500/10 to-gray-700/10 hover:from-gray-500/20 hover:to-gray-700/20';
  }
};

const getText = (status: any) => {
  switch (status) {
    case 100:
      return '待支付';
    case 200:
      return '交易成功-已出票';
    case 300:
      return '交易关闭';
    case 400:
      return '交易取消';
    default:
      return '';
  }
};

const getOrders = async () => {
  try {
    const response = await axios.post('/api/orders', {
      pageNum: currentPage.value,
      pageSize: pageSize.value,
      type: orderType.value
    });
    if (response.data.code === 200) {
      const getData = response.data.data;
      currentPage.value = getData.pageNum;
      pageSize.value = getData.pageSize;
      total.value = getData.total;
      orders.value = getData.rows;
    } else {
      message.error(response.data.msg);
    }
  } catch (error) {
    message.error('请求异常，请检查网络');
  }
}
onMounted(() => {
  getOrders();
})
</script>

<style scoped>
/* 隐藏滚动条但保留滚动功能 */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

@media (min-width: 1920px) {
  .custom-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>