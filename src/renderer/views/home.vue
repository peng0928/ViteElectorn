<template>
  <div class="pb-10">
    <div>
      <a-carousel autoplay>
        <div v-for="item in headShop" class="rounded-2xl h-75 w-full ">
          <div class="flex justify-center items-center rounded-2xl h-full">
            <img :src="item.imgUrl" class="w-[90%] h-full rounded-2xl transition-transform hover:scale-103 duration-500"
              alt="">
          </div>
        </div>
      </a-carousel>
    </div>
    <div class="flex justify-between mt-5">
      <h2>
        热卖专区
      </h2>
      <h4>
        查看更多
      </h4>
    </div>
    <div>
      <div @mousemove="handleMouseMove" @mouseleave="stopAutoScroll" ref="scrollContainer" @wheel.prevent="handleWheel"
        class="p-5 flex gap-5 w-full overflow-x-auto scrollbar-hide">
        <div class="w-64 rounded-b-2xl transform duration-500 hover:-translate-y-2 shadow-xl" v-for="item in hotShop"
          :key="item.id">
          <div class="lg:w-45 sm:w-32  flex-shrink-0 hover:ring-3 hover:ring-black  rounded-2xl">
            <div class="content bg-cover bg-center lg:h-64 sm:h-32 rounded-2xl"
              :style="{ backgroundImage: `url(${item.posterUrl})` }"></div>
            <div class="px-4 pb-3">
              <div class="mt-3 lg:text-md text-gray-700 line-clamp-2">{{ item.name }}</div>
              <div class="lg:text-xl text-red-700">{{ item.lowestPrice }}</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

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

// 保留原有的滚轮处理
const handleWheel = (e: WheelEvent) => {
  if (!scrollContainer.value) return
  const delta = Math.sign(e.deltaY) * 30
  scrollContainer.value.scrollLeft += delta
}
const hotShop = ref(
  [
    {
      "type": 1,
      "bizId": 2686657496,
      "projectId": 2686657496,
      "name": "【北京】2025北京返场暨收官场·林志炫ONEtake2.0《我忘了我已老去》演唱会",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "北京",
      "shortCity": "北京",
      "venueName": "华熙LIVE·五棵松·场馆",
      "lowestPrice": 480.00,
      "projectPrice": "",
      "dateRange": "2025.03.30"
    },
    {
      "type": 1,
      "bizId": 9212732159,
      "projectId": 9212732159,
      "name": "【北京】《给所有知道我名字的人》赵传2025演唱会-北京站",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1736490546448.477.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "北京",
      "shortCity": "北京",
      "venueName": "国家体育馆",
      "lowestPrice": 380.00,
      "projectPrice": "",
      "dateRange": "2025.06.14"
    },
    {
      "type": 1,
      "bizId": 6522494577,
      "projectId": 6522494577,
      "name": "【北京】早安领衔主演-中国首部大型说唱音乐剧《东楼》",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1741238737639.1204.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "北京",
      "shortCity": "北京",
      "venueName": "二七剧场",
      "lowestPrice": 280.00,
      "projectPrice": "",
      "dateRange": "2025.03.28-2025.03.29"
    },
    {
      "type": 1,
      "bizId": 5761116296,
      "projectId": 5761116296,
      "name": "【北京】麋先生 MIXER〈 马戏团运动 CircUs 〉北京演唱会",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1736328347794.750x1058.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "北京",
      "shortCity": "北京",
      "venueName": "五棵松·爱乐汇艺术空间·都市剧场",
      "lowestPrice": 158.00,
      "projectPrice": "",
      "dateRange": "2025.04.20"
    },
    {
      "type": 1,
      "bizId": 7681164166,
      "projectId": 7681164166,
      "name": "【天津】2025姜育恒永远演唱会-天津站",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1740798133635.6938.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "天津",
      "shortCity": "天津",
      "venueName": "天津奥林匹克中心体育馆",
      "lowestPrice": 380.00,
      "projectPrice": "",
      "dateRange": "2025.03.15"
    },
    {
      "type": 1,
      "bizId": 8669531351,
      "projectId": 8669531351,
      "name": "【济南】李宗盛2025『有歌之年』巡回演唱会-济南站",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1736588350053.607.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "济南",
      "shortCity": "济南",
      "venueName": "济南奥体中心体育馆",
      "lowestPrice": 580.00,
      "projectPrice": "",
      "dateRange": "2025.06.13、2025.06.15"
    },
    {
      "type": 1,
      "bizId": 7856696861,
      "projectId": 7856696861,
      "name": "【呼和浩特】刘若英【飞行日】2025 巡回演唱会-呼和浩特站",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1741314672695.3743.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "呼和浩特",
      "shortCity": "呼和浩特",
      "venueName": "国家北方足球训练基地综合馆",
      "lowestPrice": 499.00,
      "projectPrice": "",
      "dateRange": "2025.04.25-2025.04.26"
    },
    {
      "type": 1,
      "bizId": 7855684534,
      "projectId": 7855684534,
      "name": "【烟台】刘若英【飞行日】2025 巡回演唱会 烟台站",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1741315353835.3137.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "烟台",
      "shortCity": "烟台",
      "venueName": "烟台八角湾国际会展中心B3展馆",
      "lowestPrice": 499.00,
      "projectPrice": "",
      "dateRange": "2025.04.19-2025.04.20"
    },
    {
      "type": 1,
      "bizId": 2372273125,
      "projectId": 2372273125,
      "name": "【上海】2025 陈小春 生·旦·净·末·丑 巡回演唱会-上海站",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1738851944129.750-1058.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海浦发银行东方体育中心",
      "lowestPrice": 480.00,
      "projectPrice": "",
      "dateRange": "2025.05.31"
    },
    {
      "type": 1,
      "bizId": 8347736398,
      "projectId": 8347736398,
      "name": "【上海】在舞蹈中理解千年前庄子书写的神话传说《帝寤七日》",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1738907627052.纷玩岛-竖750X1058.png",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海国际舞蹈中心·实验剧场",
      "lowestPrice": 100.00,
      "projectPrice": "",
      "dateRange": "2025.03.21-2025.03.22"
    },
    {
      "type": 1,
      "bizId": 6717228231,
      "projectId": 6717228231,
      "name": "【上海】早安领衔主演-中国首部大型说唱音乐剧《东楼》",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1740042775361.微信图片_20250220171247.png",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "交通银行前滩31演艺中心•大剧场",
      "lowestPrice": 280.00,
      "projectPrice": "",
      "dateRange": "2025.04.05-2025.04.06"
    },
    {
      "type": 1,
      "bizId": 9661941293,
      "projectId": 9661941293,
      "name": "【上海】杂技儿童剧《七彩宝莲灯》",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1740990977698.375.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "宛平剧院·大剧场",
      "lowestPrice": 80.00,
      "projectPrice": "",
      "dateRange": "2025.07.05"
    },
    {
      "type": 1,
      "bizId": 9233321189,
      "projectId": 9233321189,
      "name": "【上海】阿朵原创舞台剧-《天生傲骨》",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1740374495007.8574.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海西岸大剧院-大剧场",
      "lowestPrice": 180.00,
      "projectPrice": "",
      "dateRange": "2025.03.07-2025.03.15"
    },
    {
      "type": 1,
      "bizId": 7974847241,
      "projectId": 7974847241,
      "name": "【上海】江西文演·陆川导演作品舞剧《天工开物》",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1737357800231.海报-750x1058px 5m.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "九棵树（上海）未来艺术中心-大剧场",
      "lowestPrice": 180.00,
      "projectPrice": "",
      "dateRange": "2025.05.02-2025.05.03"
    },
    {
      "type": 1,
      "bizId": 1927552172,
      "projectId": 1927552172,
      "name": "【上海】璀璨夜-世界音乐剧明星Stars演唱会",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1737524243682.ec4dcebc394c194cd8e5bcc09c97df2.png",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海西岸大剧院-大剧场",
      "lowestPrice": 180.00,
      "projectPrice": "",
      "dateRange": "2025.03.27-2025.03.30"
    },
    {
      "type": 1,
      "bizId": 7648781775,
      "projectId": 7648781775,
      "name": "【上海】2025周慧敏「地老天荒爱一场」巡回演唱会上海站",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1735204931502.183.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海体育馆",
      "lowestPrice": 588.00,
      "projectPrice": "",
      "dateRange": "2025.03.16"
    },
    {
      "type": 1,
      "bizId": 4957275894,
      "projectId": 4957275894,
      "name": "【上海】《乐来乐快乐》“方锦龙和他的朋友们”跨界国乐相声秀",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1733577825934.7625.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "宛平剧院·大剧场",
      "lowestPrice": 180.00,
      "projectPrice": "",
      "dateRange": "2025.03.28-2025.03.29"
    },
    {
      "type": 1,
      "bizId": 8656777178,
      "projectId": 8656777178,
      "name": "【上海】麋先生MIXER《马戏团运动 CircUs》世界巡回演唱会",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1736329361824.750X1058.png",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "MODERN SKY LAB上海",
      "lowestPrice": 158.00,
      "projectPrice": "",
      "dateRange": "2025.04.18"
    },
    {
      "type": 1,
      "bizId": 7899586432,
      "projectId": 7899586432,
      "name": "【上海】苏州芭蕾舞团《请记住我——芭蕾荟萃》",
      "posterUrl": "https://assetstest.livelab.com.cn/images/cloud/1738834525230.EN苏芭竖版海报.png",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海国际舞蹈中心·大剧场",
      "lowestPrice": 80.00,
      "projectPrice": "",
      "dateRange": "2025.03.28-2025.03.29"
    },
    {
      "type": 1,
      "bizId": 7838897394,
      "projectId": 7838897394,
      "name": "【上海】“永恒的巴黎圣母院”穿越时空沉浸式VR之旅",
      "posterUrl": "https://livelabassets.livelab.com.cn/images/ad/1740380982144.6738.jpg",
      "tagName": null,
      "tagRemark": null,
      "city": "上海",
      "shortCity": "上海",
      "venueName": "上海展览中心东二馆B1层",
      "lowestPrice": 198.00,
      "projectPrice": "",
      "dateRange": "2024.07.12-2025.03.31"
    }
  ]
)
const headShop = ref(
  [
    {
      "id": 12046,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1734945985762.908.jpg",
      "title": "五月天桃园周边banner",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 18,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522wyt-008%2522%257D",
      "activityType": 0
    },
    {
      "id": 12047,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1741577039188.121.png",
      "title": "黄子",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 17,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522HZHF01%2522%257D",
      "activityType": 0
    },
    {
      "id": 12048,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/homeSetting/1734789831510.5059.jpg",
      "title": "李荣浩巡演",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 16,
      "redirectType": 3,
      "redirectTarget": "https://mact.livelab.com.cn/artist.html#/index?artistId=%E6%9D%8E%E8%8D%A3%E6%B5%A9&isLogin=true",
      "activityType": 0
    },
    {
      "id": 12049,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/homeSetting/1733377727783.0586.jpg",
      "title": "张学友60+巡回演唱会纪念周边",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 15,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522zxy001%2522%257D",
      "activityType": 0
    },
    {
      "id": 12050,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1732192035211.2253.jpg",
      "title": "【正品售卖】五月天云端互动版LED2.0荧光棒",
      "showSetting": 2,
      "showStartTime": "2024-03-18 12:00:00",
      "showEndTime": "2024-04-30 00:00:00",
      "sort": 14,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522wyt001%2522%257D",
      "activityType": 0
    },
    {
      "id": 12051,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/homeSetting/1729834526253.1802.jpg",
      "title": "岛上原住民 暴躁的小咸熊",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 13,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522fwd-001%2522%257D",
      "activityType": 0
    },
    {
      "id": 12052,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725273788960.908.jpg",
      "title": "【正品售卖】你要不要变哈密瓜互动手灯",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 12,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522GWR-A%2522%257D",
      "activityType": 0
    },
    {
      "id": 12053,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725274074023.0518.png",
      "title": "【乐华娱乐】王一博Hello YiBO 周边合集",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 11,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522yhss-003%2522%257D",
      "activityType": 0
    },
    {
      "id": 12054,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725274066941.2397.png",
      "title": "【乐华娱乐】李汶翰 HVEN的礼物盒 ​周边合集",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 10,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522yhss-04%2522%257D",
      "activityType": 0
    },
    {
      "id": 12055,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1726815240802.7656.jpg",
      "title": "【周兴哲】Odyssey~巡回演唱会纪念手灯",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 9,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522zxz-001%2522%257D",
      "activityType": 0
    },
    {
      "id": 12056,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725275189666.1917.png",
      "title": "【乐华娱乐】毕雯珺 赞不落户 周边合集",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 8,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522yhss-010%2522%257D",
      "activityType": 0
    },
    {
      "id": 12057,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725274445615.6655.jpg",
      "title": "【正品售卖】五月天 和你一起长不大周边合集",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 7,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522wyt-03%2522%257D",
      "activityType": 0
    },
    {
      "id": 12058,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/homeSetting/1734944680855.8906.jpg",
      "title": "周同学潮玩系列周边",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 6,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522ztx-004%2522%257D",
      "activityType": 0
    },
    {
      "id": 12059,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/homeSetting/1734944891096.7114.jpg",
      "title": "周同学城市系列周边",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 5,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522ztx-002%2522%257D",
      "activityType": 0
    },
    {
      "id": 12060,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725273835890.883.jpg",
      "title": "【正品售卖】莫文蔚“大秀一场”演唱会纪念周边",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 4,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522MWW-B%2522%257D",
      "activityType": 0
    },
    {
      "id": 12061,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725275543260.9128.jpg",
      "title": "小岛❤️爱你哟",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 3,
      "redirectType": 5,
      "redirectTarget": "1",
      "activityType": 0
    },
    {
      "id": 12062,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/ad/1725275545171.504.jpg",
      "title": "小岛宝藏",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 2,
      "redirectType": 5,
      "redirectTarget": "2",
      "activityType": 0
    },
    {
      "id": 12063,
      "moduleId": 52,
      "type": 1,
      "imgUrl": "https://livelabassets.livelab.com.cn/images/homeSetting/1725273842143.6938.jpg",
      "title": "【预售】汪峰2024“灿烂的你”巡演独家纪念PASS卡",
      "showSetting": 2,
      "showStartTime": null,
      "showEndTime": null,
      "sort": 1,
      "redirectType": 3,
      "redirectTarget": "https://mall.livelab.com.cn/pagesB/productDetail/index?query=%257B%2522platformProductCode%2522%253A%2522wf-001%2522%257D",
      "activityType": 0
    }]
)

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
