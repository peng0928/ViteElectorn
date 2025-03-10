<template>
  <div class="h-full bg-gray-100 flex items-center justify-center p-4">
    <a-card class="w-full max-w-md shadow-lg rounded-2xl">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-800">手机验证码登录</h1>
      </div>

      <a-form :model="form" @submit="handleSubmit" layout="vertical">
        <!-- 手机号码输入 -->
        <a-form-item
          label="手机号码"
          name="phone"
          :rules="[
            { required: true, message: '请输入手机号码' },
            { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码' }
          ]"
        >
          <a-input
            v-model:value="form.phone"
            placeholder="请输入手机号码"
            class="w-full"
            size="large"
          >
            <template #prefix>
              <mobile-outlined class="text-gray-400" />
            </template>
          </a-input>
        </a-form-item>

        <!-- 验证码输入 -->
        <a-form-item
          label="验证码"
          name="captcha"
          :rules="[
            { required: true, message: '请输入验证码' },
            { len: 6, message: '验证码为6位数字' }
          ]"
        >
          <div class="flex gap-2">
            <a-input
              v-model:value="form.captcha"
              placeholder="请输入6位验证码"
              class="flex-1"
              size="large"
            >
              <template #prefix>
                <mail-outlined class="text-gray-400" />
              </template>
            </a-input>

            <a-button
              type="primary"
              size="large"
              :disabled="countdown > 0"
              @click="sendCaptcha"
              class="w-32"
            >
              {{ countdownText }}
            </a-button>
          </div>
        </a-form-item>

        <!-- 登录按钮 -->
        <a-button
          type="primary"
          html-type="submit"
          block
          size="large"
          :loading="loading"
          class="mt-4"
        >
          立即登录
        </a-button>
      </a-form>

      <div class="mt-6 text-center text-sm text-gray-500">
        注册即表示同意
        <a href="#" class="text-blue-500 hover:underline">用户协议</a>
        和
        <a href="#" class="text-blue-500 hover:underline">隐私政策</a>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { MobileOutlined, MailOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';

// 表单数据
const form = ref({
  phone: '',
  captcha: ''
});

// 加载状态
const loading = ref(false);
// 倒计时
const countdown = ref(0);

// 计算倒计时文本
const countdownText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}秒后重发` : '获取验证码';
});

// 发送验证码
const sendCaptcha = async () => {
  if (!/^1[3-9]\d{9}$/.test(form.value.phone)) {
    message.error('请输入正确的手机号码');
    return;
  }

  // 模拟发送验证码
  try {
    countdown.value = 60;
    const timer = setInterval(() => {
      countdown.value -= 1;
      if (countdown.value <= 0) {
        clearInterval(timer);
      }
    }, 1000);

    message.success('验证码已发送');
  } catch (error) {
    message.error('发送失败，请重试');
  }
};

// 提交表单
const handleSubmit = async () => {
  loading.value = true;
  try {
    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 1000));
    message.success('登录成功');
  } catch (error) {
    message.error('登录失败');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* 覆盖 Ant Design 默认样式 */
:deep(.ant-input-affix-wrapper) {
  @apply rounded-lg hover:border-blue-400 focus:border-blue-400;
}

:deep(.ant-btn-primary) {
  @apply bg-blue-500 hover:bg-blue-600 !important;
}
</style>