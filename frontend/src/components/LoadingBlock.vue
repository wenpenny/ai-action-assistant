<template>
  <div class="loading-block">
    <van-loading type="spinner" size="48px" />
    <p class="loading-text">加载中...</p>
  </div>
</template>

<script setup lang="ts">
// LoadingBlock 组件
</script>

<style scoped>
.loading-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  min-height: 300px;
}

.loading-text {
  margin-top: 16px;
  font-size: 16px;
  color: #666;
}
</style>