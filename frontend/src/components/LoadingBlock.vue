<template>
  <div class="loading-block">
    <van-loading type="spinner" color="#1989fa" size="36px" />
    <p class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  text?: string;
}>();
</script>

<style scoped>
.loading-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-text {
  margin-top: 16px;
  font-size: 16px;
  color: #666;
}
</style>
