<template>
  <div class="history">
    <van-nav-bar title="历史记录" fixed />
    <div class="content">
      <HistoryList />
    </div>
  </div>
</template>

<script setup lang="ts">
import HistoryList from '../components/HistoryList.vue';
</script>

<style scoped>
.history {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 60px;
}
</style>
