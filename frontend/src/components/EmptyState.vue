<template>
  <div class="empty-state">
    <van-icon name="info-o" size="48" color="#999" />
    <p class="empty-text">{{ text }}</p>
    <slot name="action"></slot>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  text: string;
}>();
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-text {
  margin-top: 16px;
  font-size: 16px;
  color: #999;
}
</style>
