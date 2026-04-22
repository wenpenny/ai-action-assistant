<template>
  <van-card :border="false" class="summary-card">
    <template #title>
      <div class="card-title">
        <van-icon name="lightbulb-o" class="title-icon" />
        <span>AI 摘要</span>
      </div>
    </template>
    <div class="summary-content">
      <p v-if="summary" class="summary-text">{{ summary }}</p>
      <p v-else class="no-summary">暂无摘要信息</p>
    </div>
  </van-card>
</template>

<script setup lang="ts">
defineProps<{
  summary: string
}>();
</script>

<style scoped>
.summary-card {
  margin-bottom: 20px;
}

.card-title {
  display: flex;
  align-items: center;
}

.title-icon {
  margin-right: 8px;
  color: #1890ff;
}

.summary-content {
  padding-top: 10px;
}

.summary-text {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  margin: 0;
}

.no-summary {
  font-size: 14px;
  color: #999;
  margin: 0;
  font-style: italic;
}
</style>