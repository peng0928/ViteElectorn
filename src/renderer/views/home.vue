<template>
  <div class="pb-10">
    <div>
      <a-carousel autoplay v-if="headShop.length > 0">
        <div v-for="item in headShop" :key="item.id" class="rounded-2xl h-65 w-full">
          <div class="flex justify-center items-center rounded-2xl h-full">
            <img :src="encodeURIfunc(item.imgUrl)"
                  loading="lazy"
                 class="w-[90%] h-full rounded-2xl transition-transform hover:scale-103 duration-500 cursor-pointer" alt="">
          </div>
        </div>
      </a-carousel>
      <div v-else class="rounded-2xl h-75 w-full overflow-hidden">
        <!-- 科技感骨架屏 -->
        <div class="h-full w-full animate-gradient-x">
          <a-skeleton active :paragraph="{ rows: 8 }" class="rounded-2xl bg-opacity-0">
            <a-skeleton-image class="w-full h-full rounded-2xl bg-opacity-0"/>
          </a-skeleton>
        </div>
      </div>
    </div>
    <div class="flex justify-between mt-5">
      <h2 class="font-bold text-2xl text-gray-800">热卖专区</h2>
      <h4>
        查看更多
      </h4>
    </div>
    <div>
      <div v-if="hotShop.length > 0">
        <div @mousemove="handleMouseMove" @mouseleave="stopAutoScroll" ref="scrollContainer"
             @wheel.prevent="handleWheel" class="p-5 flex gap-5 w-full overflow-x-auto scrollbar-hide">
          <div class="cursor-pointer w-64 rounded-b-2xl transform duration-500 hover:-translate-y-2 shadow-xl"
               v-for="item in hotShop"
               :key="item.id">
            <div class="lg:w-45 sm:w-32  flex-shrink-0 hover:ring-3 hover:ring-black  rounded-2xl"
                 @click="rPush(item.projectId)">
              <div class="content bg-cover bg-center lg:h-64 sm:h-32 rounded-2xl">
                <img :src="encodeURIfunc(item.posterUrl)" class="w-full lg:h-64 sm:h-32 rounded-2xl object-cover"
                     alt="演唱会图片" loading="lazy" />
              </div>
              <div class="px-4 pb-3">
                <div class="mt-3 lg:text-md text-gray-700 line-clamp-2">{{ item.name }}</div>
                <div class="lg:text-xl text-red-700">{{ item.lowestPrice }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="rounded-2xl h-75 w-full overflow-hidden">
        <!-- 科技感骨架屏 -->
        <div class="h-full w-full animate-gradient-x">
          <a-skeleton active :paragraph="{ rows: 8 }" class="rounded-2xl bg-opacity-0">
            <a-skeleton-image class="w-full h-full rounded-2xl bg-opacity-0"/>
          </a-skeleton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, onUnmounted} from 'vue'
import axios from 'axios';
import {message} from 'ant-design-vue';
import {useRouter} from 'vue-router';

const router = useRouter()
const scrollContainer = ref<HTMLElement | null>(null)
const autoScrollInterval = ref<number | null>(null)
const scrollSpeed = ref(0)
const showLeftIndicator = ref(false)
const showRightIndicator = ref(false)

// 鼠标移动处理
const handleMouseMove = (e: MouseEvent) => {
  if (!scrollContainer.value) return

  const containerRect = scrollContainer.value.getBoundingClientRect()
  const mouseX = e.clientX - containerRect.left
  const containerWidth = containerRect.width

  // 计算热区范围（两侧各 20%）
  const hotZoneWidth = containerWidth * 0.2

  // 判断位置
  if (mouseX < hotZoneWidth) {
    // 左侧热区
    scrollSpeed.value = -mapRange(mouseX, 0, hotZoneWidth, 15, 5)
    showLeftIndicator.value = true
    showRightIndicator.value = false
  } else if (mouseX > containerWidth - hotZoneWidth) {
    // 右侧热区
    scrollSpeed.value = mapRange(mouseX, containerWidth - hotZoneWidth, containerWidth, 5, 15)
    showLeftIndicator.value = false
    showRightIndicator.value = true
  } else {
    // 中间区域
    scrollSpeed.value = 0
    showLeftIndicator.value = false
    showRightIndicator.value = false
  }
  startAutoScroll()
}

// 数值映射
const mapRange = (value: number, inMin: number, inMax: number, outMin: number, outMax: number) => {
  return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
}

// 启动自动滚动
const startAutoScroll = () => {
  if (autoScrollInterval.value) return

  autoScrollInterval.value = window.setInterval(() => {
    if (scrollContainer.value && scrollSpeed.value !== 0) {
      scrollContainer.value.scrollLeft += scrollSpeed.value
    }
  }, 16) // 约60fps
}

// 停止自动滚动
const stopAutoScroll = () => {
  if (autoScrollInterval.value) {
    clearInterval(autoScrollInterval.value)
    autoScrollInterval.value = null
  }
  scrollSpeed.value = 0
  showLeftIndicator.value = false
  showRightIndicator.value = false
}

// 清理
onUnmounted(() => {
  stopAutoScroll()
})

onMounted(() => {
  gethotShop();
  getheadShop();
})

// 保留原有的滚轮处理
const handleWheel = (e: WheelEvent) => {
  if (!scrollContainer.value) return
  const delta = Math.sign(e.deltaY) * 30
  scrollContainer.value.scrollLeft += delta
}
const hotShop = ref(
    []
)
const headShop = ref(
    []
)


const gethotShop = async () => {
  try {
    const response = await axios.post('/api/hotShop', {});
    if (response.data.code === 200) {
      hotShop.value = response.data.data;
    }
  } catch (error) {
    message.error('请求异常，请检查网络');
  }
}
const getheadShop = async () => {
  try {
    const response = await axios.post('/api/headShop', {});
    if (response.data.code === 200) {
      headShop.value = response.data.data;
    }
  } catch (error) {
    message.error('请求异常，请检查网络');
  }
}

const encodeURIfunc = (url: any) => {
  const res = encodeURI(url);
  return res;
}
const rPush = (id: any) => {
  router.push({name: 'project', params: {params: id}});
}
</script>


<style scoped>
/* 隐藏所有浏览器滚动条 */
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
