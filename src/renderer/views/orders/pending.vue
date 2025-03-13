<template>
    <div class="p-5 pb-15">
        <!-- 页面标题 -->
        <div class="mb-1">
            <h2 class="font-bold text-2xl text-gray-800">订单管理</h2>
        </div>

        <!-- 筛选条件 -->
        <div class="mb-1 flex space-x-4">
            <button v-for="option in filterOptions" :key="option.value" @click="filterStatus = option.value" :class="[
                'px-6 py-2 rounded-lg border-2 transition-all duration-300',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                filterStatus === option.value
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

        <!-- 订单列表 -->
        <div
            class="p-5 grid gap-12 2xl:grid-cols-4 xl:grid-cols-3 lg:grid-cols-2 md:grid-cols-1 sm:grid-cols-1 xs:grid-cols-1 h-[calc(100vh-280px)] overflow-y-auto scrollbar-hide rounded-2xl">
            <div v-for="order in paginatedOrders" :key="order.id" :class="[
                'relative h-64 w-72 p-4 rounded-lg transition-all duration-300',
                'hover:scale-105 hover:shadow-2xl rounded-2xl',
                getCardBackground(order.status),
            ]">
                <!-- 票面内容 -->
                <div class="flex h-full w-full">
                    <div class="h-full w-38">
                        <img :src="order.image" class="w-full h-full rounded-lg object-cover" alt="演唱会图片" />
                    </div>
                    <div class="ml-3 p-2 w-2/3">
                        <h3 class="text-md font-bold text-gray-800 line-clamp-2">{{ order.title }}</h3>
                        <div class="text-gray-600 mt-2">
                            <div>{{ order.location }}</div>
                            <div>{{ order.date }}</div>
                        </div>
                    </div>
                </div>

                <div class="absolute bottom-10 right-4">
                    <a-tag :color="getStatusColor(order.status)">
                        <template #icon>
                            <div class="flex items-center align-middle">
                                <icon :icon="getStatusIcon(order.status)" class="text-md" />
                                {{ order.status }}
                            </div>
                        </template>
                    </a-tag>
                </div>
                <!-- 状态标签 -->
                <div class="absolute bottom-4 right-4">
                    <a-tag :color="getStatusColor(order.status)">
                       2025-03-13 20:08
                    </a-tag>
                </div>
            </div>
        </div>

        <!-- 分页 -->
        <div class="mt-6 flex justify-center">
            <a-pagination v-model:current="currentPage" v-model:pageSize="pageSize" :total="filteredOrders.length"
                :pageSizeOptions="['8', '12', '24', '48']" show-less-items show-size-changer @change="handlePageChange"
                @showSizeChange="handlePageChange" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 订单数据
const orders = ref([
    { id: 1, title: '【北京】2025北京返场暨收官场·林志炫ONEtake2.0《我忘了我已老去》演唱会', location: '北京 华熙LIVE·五棵松·场馆', date: '2024/08/24 19:30', status: 'collecting', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 2, title: '【上海】2025上海站·周杰伦《嘉年华》演唱会', location: '上海 梅赛德斯奔驰文化中心', date: '2024/09/15 20:00', status: 'completed', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 3, title: '【广州】2025广州站·五月天《人生无限公司》演唱会', location: '广州 天河体育中心', date: '2024/10/10 19:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 4, title: '【深圳】2025深圳站·陈奕迅《FEAR AND DREAMS》演唱会', location: '深圳 大运中心', date: '2024/11/05 20:00', status: 'collecting', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 5, title: '【成都】2025成都站·张学友《60+》演唱会', location: '成都 双流体育中心', date: '2024/12/12 19:30', status: 'completed', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
    { id: 6, title: '【武汉】2025武汉站·蔡依林《UGLY BEAUTY》演唱会', location: '武汉 光谷国际网球中心', date: '2025/01/01 20:00', status: 'error', image: 'https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg' },
]);

// 筛选状态
const filterStatus = ref('all');

// 筛选选项
const filterOptions = [
    { value: 'all', label: '全部', icon: 'ri:list-unordered' },
    { value: 'collecting', label: '购票中', icon: 'line-md:loading-twotone-loop' },
    { value: 'completed', label: '购票完成', icon: 'mdi:sticker-check-outline' },
    { value: 'error', label: '购票异常', icon: 'icon-park-outline:error' },
];

// 分页相关
// 分页相关
const currentPage = ref(1);
const pageSize = ref(8);

// 分页后的订单数据
const paginatedOrders = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    return filteredOrders.value.slice(start, end);
});

// 处理分页变化
const handlePageChange = (page: number, size: number) => {
    currentPage.value = page;
    pageSize.value = size;
};
// 根据筛选状态过滤订单
const filteredOrders = computed(() => {
    if (filterStatus.value === 'all') {
        return orders.value;
    }
    return orders.value.filter(order => order.status === filterStatus.value);
});


// 获取状态标签颜色
const getStatusColor = (status: string) => {
    switch (status) {
        case 'collecting':
            return 'blue';
        case 'completed':
            return 'green';
        case 'error':
            return 'red';
        default:
            return 'gray';
    }
};

// 获取状态图标
const getStatusIcon = (status: string) => {
    switch (status) {
        case 'collecting':
            return 'line-md:loading-twotone-loop';
        case 'completed':
            return 'icon-park-outline:check';
        case 'error':
            return 'icon-park-outline:error';
        default:
            return 'ri:list-unordered';
    }
};

// 获取卡片背景
const getCardBackground = (status: string) => {
    switch (status) {
        case 'collecting':
            return 'bg-gradient-to-r from-blue-500/10 to-purple-500/10 hover:from-blue-500/20 hover:to-purple-500/20';
        case 'completed':
            return 'bg-gradient-to-r from-green-500/10 to-teal-500/10 hover:from-green-500/20 hover:to-teal-500/20';
        case 'error':
            return 'bg-gradient-to-r from-red-500/10 to-pink-500/10 hover:from-red-500/20 hover:to-pink-500/20';
        default:
            return 'bg-gradient-to-r from-gray-500/10 to-gray-700/10 hover:from-gray-500/20 hover:to-gray-700/20';
    }
};
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