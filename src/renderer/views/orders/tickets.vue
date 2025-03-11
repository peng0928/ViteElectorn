<template>
  <div class="p-5 pb-15">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h2 class="font-bold text-2xl text-gray-800">我的票夹</h2>
    </div>

    <!-- 票夹列表 -->
    <div class="grid gap-6 xl:grid-cols-3 2xl:grid-cols-4 lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1 xs:grid-cols-1">
      <div
        class="relative h-64 w-72 p-4 rounded-2xl transition-transform hover:scale-105 duration-300 bg-gradient-to-r from-blue-600/50 to-purple-600/50 hover:from-blue-700/60 hover:to-purple-700/60 shadow-lg">
        <!-- 票面内容 -->
        <div class="flex h-full w-full">
          <div class="h-full w-38">
            <img src="https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg"
              class="w-full h-[80%] rounded-2xl object-cover" alt="演唱会图片" />
          </div>
          <div class="ml-3 p-2 w-2/3">
            <h3 class="text-md font-bold text-gray-800 line-clamp-2">
              【北京】2025北京返场暨收官场·林志炫ONEtake2.0《我忘了我已老去》演唱会
            </h3>
            <div class="text-gray-600 mt-2">
              <div>北京 华熙LIVE·五棵松·场馆</div>
              <div>2024/08/24 19:30</div>
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
        <div class="absolute top-[75%] w-4 h-4 right-15 -translate-y-1/2 rounded-2xl">
          <img src="/utils/img/end.svg" alt="状态图标" />
        </div>

        <!-- 底部提示 -->
        <div class="absolute top-[88%]">
          <div class="text-nowrap text-gray-600">请携带身份证原价直刷进场</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 这里可以添加逻辑代码
</script>

<style scoped>
svg path {
  fill: #008095;
}
</style>