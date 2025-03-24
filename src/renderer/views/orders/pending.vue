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
                        <icon :icon="option.icon" class="text-md" />
                    </div>
                    <div>{{ option.label }}</div>
                </div>
            </button>
        </div>

        <div
            class="p-5 grid gap-15 flex flex-wrap  inline-flex cursor-pointer overflow-y-auto scrollbar-hide rounded-2xl max-h-[calc(100vh-260px)]">
            <div v-for="(order, index) in paginatedOrders" :key="order.id" :class="[
                'relative h-76 w-120 p-5 rounded-lg transition-all duration-300',
                ' hover:scale-101 hover:shadow-2xl rounded-2xl',
                getCardBackground(order.spider_status),
            ]">
                <!-- 索引标签 -->
                <div
                    class="absolute -top-3 -left-3 w-8 h-8 flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold text-lg rounded-full shadow-lg glow">
                    {{ index + 1 }}
                </div>
                <!-- 票面内容 -->
                <div class="flex h-full w-full">
                    <div class="relative overflow-hidden rounded-lg shadow-2xl  w-2/5">
                        <img :src="order.poster" class="w-full h-full rounded-lg" alt="演唱会图片" />
                    </div>


                    <div class="ml-3 p-2 w-2/3 flex flex-col">
                        <div class="font-bold flex justify-center items-center gap-4 p-2 ">
                            <div class="gap-4">
                                <div class="text-xl font-mono">{{ order.name }}</div>
                                <div class="text-xl font-mono">{{ order.startDate }}</div>
                            </div>
                        </div>
                        <div class="font-bold flex justify-center items-center gap-4 p-2 mt-auto">
                            <div class="text-xl text-blue-500 font-mono w-24">状态</div>
                            <div class="text-sm font-mono flex-1">{{ getText(order.spider_status) }}</div>
                        </div>
                        <div class="font-bold flex justify-center items-center gap-4 p-2">
                            <div class="text-xl text-blue-500 font-mono w-24">任务时间</div>
                            <div class="text-sm font-mono flex-1">{{ order.create_time }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <!-- 分页 -->
        <div class="mt-6 flex justify-center">
            <a-pagination v-model:current="currentPage" v-model:pageSize="pageSize" :total="total"
                :pageSizeOptions="['5', '10', '20', '50']" show-less-items show-size-changer @change="handlePageChange" />
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { message } from 'ant-design-vue';
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '../../stores/userStore';

const userStore = useUserStore();

// 订单数据
const orders = ref([]);

// 筛选状态
const filterStatus = ref('all');


const filterOptions = [
    { value: 'all', type: 200, label: '全部', icon: 'ri:list-unordered' },
    { value: [2], type: 2, label: '完成', icon: 'material-symbols:check' },
    { value: [0], type: 0, label: '未开始', icon: 'icon-park-solid:flash-payment' },
    { value: [1], type: 1, label: '进行中', icon: 'icon-park-solid:flash-payment' },
    { value: [3, 4], type: 3, label: '异常', icon: 'material-symbols-light:cancel' },
];

// 分页相关
// 分页相关
const currentPage = ref(1);
const pageSize = ref(5);
const total = ref(0);
const orderType = ref(200);

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
    const data = orders.value.filter(order => filterStatus.value.includes(order.spider_status));
    return data;
});


// 获取状态标签颜色
const getStatusColor = (status: any) => {
    switch (status) {
        case 1:
            return 'blue';
        case 2:
            return 'green';
        case 3:
            return 'red';
        case 3:
            return 'red';
        case 0:
            return 'red';
    }
};

// 获取状态图标
const getStatusIcon = (status: any) => {
    switch (status) {
        case 1:
            return 'line-md:loading-twotone-loop';
        case 2:
            return 'material-symbols:check';
        case 3:
            return 'icon-park-outline:error';
        case 3:
            return 'icon-park-outline:error';
        default:
            return 'ri:list-unordered';
    }
};

// 获取卡片背景
const getCardBackground = (status: any) => {
    switch (status) {
        case 1:
            return 'bg-gradient-to-r from-blue-3 to-purple-3 hover:from-blue-4 hover:to-purple-3    ';
        case 2:
            return 'bg-gradient-to-r from-green-3 to-teal-3 hover:from-green-4 hover:to-teal-3';
        case 3:
            return 'bg-gradient-to-r from-red-3 to-green-3 hover:from-red-4 hover:to-green-3';
        case 3:
            return 'bg-gradient-to-r from-red-700/10 to-pink-700/10 hover:from-red-700/20 hover:to-pink-700/20';
        default:
            return 'bg-gradient-to-r from-gray-3 to-gray-3 hover:from-gray-4 hover:to-gray-3';
    }
};

const getText = (status: any) => {
    switch (status) {
        case 1:
            return '进行中';
        case 2:
            return '已完成';
        case 3:
            return '账号掉线';
        case 4:
            return '采集异常';
        case 0:
            return '未开始';
    }
};

const getOrders = async () => {
    try {
        const response = await axios.post('/api/task/find', {
            page: currentPage.value,
            pageSize: pageSize.value,
            type: orderType.value,
            data: { uid: userStore.userInfo.uid }
        });
        if (response.data.code === 200) {
            const getData = response.data.data;
            currentPage.value = getData.pageNum;
            pageSize.value = getData.pageSize;
            total.value = getData.total;
            orders.value = getData.data;
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
</style>