<template>
  <div class="p-5 pb-15">
    <div>
      <h2 class="font-bold text-xl ">我的票夹</h2>
    </div>
    <div class="">
      <div
          class="px-5 grid gap-10 xl:grid-cols-3 2xl:grid-cols-4 lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1 xs:grid-cols-1 w-full">
        <div
            class="relative h-64 w-72 bg-[#8261ef] p-3 rounded-2xl shadow-2xl transition-transform hover:scale-105 duration-500">
          <!-- 票面内容 -->
          <div class="flex h-full w-full">
            <div class="h-full w-38">
              <img
                  src="https://assetstest.livelab.com.cn/images/cloud/1735198359996.纷玩岛750-1058.jpg"
                  class="w-full h-[80%] rounded-2xl "
                  alt=""
              >
            </div>
            <div class="ml-3 p-2 w-3/5">
              <h3 class="text-md font-bold text-black line-clamp-2">
                【北京】2025北京返场暨收官场·林志炫ONEtake2.0《我忘了我已老去》演唱会</h3>
              <div class="text-gray-8">
                <div>北京 华熙LIVE·五棵松·场馆</div>
                <div>2024/08/24 19:30</div>
              </div>
            </div>
          </div>

          <!-- 虚线分割线 -->
          <div class="absolute left-0 w-full top-[80%] border-b-2 border-dotted border-[#f1a15a]"></div>

          <!-- 左侧缺口 -->
          <div class="absolute top-[81%] -left-2 w-4 h-4 bg-white -translate-y-1/2 rounded-2xl"></div>

          <!-- 右侧缺口 -->
          <div class="absolute top-[81%] -right-2 w-4 h-4 bg-white -translate-y-1/2 rounded-2xl"></div>
          <div class="absolute top-[75%] w-4 h-4 right-15 -translate-y-1/2 rounded-2xl ">
            <img
                src="/utils/img/end.svg"
                alt=""
            >
          </div>
          <div class="absolute top-[88%]">
            <div class="text-nowrap text-gray-8">请携带身份证原价直刷进场</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">

</script>

<style scoped>
svg path {
  fill: #008095;
}
</style>