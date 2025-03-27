<template>
    <div class="min-h-screen text-gray-100 p-6 font-sans rounded-xl">
        <!-- 上半部分：数据介绍 -->
        <div class="h-[50vh] mb-6 flex flex-col md:flex-row gap-6">
            <!-- 左侧图片 -->
            <div
                class="md:w-1/5 h-full bg-gradient-to-br from-blue-900 to-indigo-800 rounded-xl flex items-center justify-center relative overflow-hidden">
                <img :src="data.poster" class="w-full h-full rounded-lg">
                <!-- <h2 class="text-2xl font-bold mb-2">系统监控面板</h2> -->
                <!-- <p class="text-indigo-200">实时数据可视化分析平台</p> -->
            </div>

            <!-- 右侧详情 -->
            <div class="md:w-4/5 h-full flex flex-col">
                <div class="bg-gray-800 rounded-xl p-6 flex-1 flex flex-col">
                    <h2 class="text-xl font-bold mb-6 flex items-center">
                        <span class="w-3 h-3 rounded-full bg-green-100 mr-2 animate-pulse"></span>
                        {{ data.name }}
                    </h2>

                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <div v-for="item in stats" :key="item.title" class="bg-gray-700/50 rounded-lg p-4 border-l-4"
                            :class="`border-${item.color}-500`">
                            <h3 class="text-sm text-gray-400 mb-1">{{ item.title }}</h3>
                            <p class="text-2xl font-mono">{{ data[item.value] }}</p>
                        </div>
                    </div>

                    <div class="mt-auto">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-gray-400">最后更新时间</span>
                            <span class="font-mono">{{ currentTime }}</span>
                        </div>
                        <div class="h-1.5 w-full bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"
                                :style="{ width: `${syncProgress}%` }"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 下半部分：日志区域 -->
        <div class="h-[50vh] bg-gray-800 rounded-xl p-6 flex flex-col">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-bold flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-400" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    实时日志
                </h2>
                <div class="flex items-center">
                    <span class="text-xs px-2 py-1 bg-gray-700 rounded mr-2">{{ logs.length }} 条记录</span>
                    <button @click="autoScroll = !autoScroll" class="text-xs px-2 py-1 rounded"
                        :class="autoScroll ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'">
                        {{ autoScroll ? '自动滚动中' : '暂停滚动' }}
                    </button>
                </div>
            </div>

            <div ref="logContainer" class="flex-1 overflow-y-auto font-mono text-sm bg-gray-900 rounded-lg p-4 space-y-3">
                <div v-for="(log, index) in logs" :key="index" class="flex">
                    <span class="text-gray-500 w-32 shrink-0">{{ log.time }}</span>
                    <span class="text-gray-400 mr-3">[{{ log.source }}]</span>
                    <span :class="getLogLevelClass(log.level)">{{ log.message }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { message } from 'ant-design-vue';
import axios from 'axios';
import { ref, computed, onMounted, onBeforeUnmount, nextTick, } from 'vue'
import { useRoute } from 'vue-router';

const route = useRoute();
const params = ref(route.params.params);

interface StatItem {
    title: string
    value: string
    color: string
}

interface LogItem {
    time: string
    source: string
    level: string
    message: string
}

// 统计数据
const stats = ref<StatItem[]>([
    { title: '开始日期', value: 'startDate', color: 'green' },
    { title: '场馆', value: 'startDate', color: 'green' },
    { title: '已选坐席', value: '看台655元', color: 'blue' },
    { title: '购票人员', value: '78%', color: 'yellow' },
    { title: '任务状态', value: 'spider_status', color: 'indigo' },
])

// 当前时间
const currentTime = computed(() => {
    return new Date().toLocaleTimeString()
})

// 同步进度
const syncProgress = ref(0)
const syncInterval = ref<NodeJS.Timeout>()

// 日志相关
const logContainer = ref<HTMLElement>()
const autoScroll = ref(true)
const logs = ref<LogItem[]>([])
const data = ref({})

// 生成随机日志
function generateRandomLog(): LogItem {
    const levels = ['INFO', 'WARN', 'ERROR', 'DEBUG']
    const sources = ['System', 'Network', 'Database', 'Security', 'API']
    const messages = [
        'Initializing system components',
        'Database connection established',
        'High CPU usage detected',
        'New device connected to network',
        'Security scan completed',
        'Failed to authenticate user',
        'Backup process started',
        'Memory leak detected in service',
        'System update available',
        'Firewall rules updated'
    ]

    return {
        time: new Date().toLocaleTimeString(),
        source: sources[Math.floor(Math.random() * sources.length)],
        level: levels[Math.floor(Math.random() * levels.length)],
        message: messages[Math.floor(Math.random() * messages.length)]
    }
}

// 根据日志级别获取样式类
function getLogLevelClass(level: string): string {
    switch (level) {
        case 'INFO': return 'text-blue-400'
        case 'WARN': return 'text-yellow-400'
        case 'ERROR': return 'text-red-400'
        case 'DEBUG': return 'text-purple-400'
        default: return 'text-gray-300'
    }
}

// 滚动到底部
function scrollToBottom() {
    if (logContainer.value && autoScroll.value) {
        nextTick(() => {
            logContainer.value!.scrollTop = logContainer.value!.scrollHeight
        })
    }
}


const getTask = async () => {
    try {
        const response = await axios.post('/api/task/m5/find', {
            m5: params.value
        });
        if (response.data.code === 200) {
            const getData = response.data.data;
            console.log(getData)
            data.value = getData;
        } else {
            message.error(response.data.msg);
        }
    } catch (error) {
        message.error('请求异常，请检查网络');
    }
}
// 初始化
onMounted(() => {
    // 初始化一些日志
    getTask();
    for (let i = 0; i < 15; i++) {
        logs.value.push(generateRandomLog())
    }

    // 更新同步进度
    syncInterval.value = setInterval(() => {
        syncProgress.value = (syncProgress.value + 5) % 100
    }, 1000)

    // 定时添加新日志
    const logInterval = setInterval(() => {
        if (logs.value.length > 50) {
            logs.value.shift()
        }
        logs.value.push(generateRandomLog())
        scrollToBottom()
    }, 1500)

    // 更新时间
    const timeInterval = setInterval(() => {
        // 时间更新会通过计算属性自动处理
    }, 1000)

    onBeforeUnmount(() => {
        clearInterval(syncInterval.value)
        clearInterval(logInterval)
        clearInterval(timeInterval)
    })
})
</script>
  
<style>
/* 自定义滚动条 */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
</style>