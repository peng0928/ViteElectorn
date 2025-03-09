<script setup lang="ts">

</script>


<template>
  <div>
    <h2>
      演唱会
    </h2>
    <!-- article[@class='mx-auto group w-full shadow-2xl max-w-md pb-8 rounded-b-2xl transform duration-500 hover:-translate-y-2 cursor-pointer group']/
      section[@class='content bg-cover bg-center h-64 rounded-2xl']/
      div[@class='flex items-end w-full h-full bg-black bg-opacity-20 text-white text-sm font-bold p-4 rounded-2xl'] -->
    <div>
      <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-10">
        <article
          class="mx-auto group w-full shadow-2xl max-w-md rounded-b-2xl transform duration-500 hover:-translate-y-2 cursor-pointer">
          <section class="content bg-cover bg-center h-64 rounded-2xl"
            style="background-image: url(https://img.alicdn.com/bao/uploaded/i2/2251059038/O1CN019QyBif2GdSg9JXhrQ_!!4611686018427383646-0-item_pic.jpg);">
            <div
              class="flex items-end w-full h-full bg-black bg-opacity-20 text-white text-sm font-bold p-4 rounded-2xl">
            </div>
          </section>
          <div class="px-4 pb-3">
            <div class="mt-3 text-xl text-gray-700">爽子20周年北展音乐会 </div>
            <div class=" text-xl text-red-700">¥480起 </div>
          </div>
        </article>


      </section>

    </div>
  </div>
</template>

<style scoped></style>
