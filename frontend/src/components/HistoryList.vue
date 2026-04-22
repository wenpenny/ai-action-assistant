<template>
  <div class="history-list">
    <van-list
      v-model:loading="loading"
      :finished="finished"
      finished-text="没有更多记录了"
      @load="loadHistory"
    >
      <van-cell
        v-for="item in historyItems"
        :key="item.image.id"
        class="history-item"
        @click="goToDetail(item.image.id)"
      >
        <div class="item-content">
          <div class="item-left">
            <van-image
              :src="getImageUrl(item.image.file_name)"
              fit="cover"
              class="item-image"
            />
          </div>
          <div class="item-right">
            <div class="item-header">
              <van-tag :color="getSceneColor(item.parse_result?.scene_type)" size="small">{{ getSceneLabel(item.parse_result?.scene_type) }}</van-tag>
              <span class="item-time">{{ formatDate(item.image.created_at) }}</span>
            </div>
            <h3 class="item-title">{{ item.parse_result?.entities?.title || '未识别' }}</h3>
            <p class="item-summary">{{ item.parse_result?.summary || '无解析结果' }}</p>
            <div class="item-actions" v-if="item.action_records.length > 0">
              <span class="action-count">{{ item.action_records.length }} 个动作</span>
            </div>
          </div>
        </div>
      </van-cell>
    </van-list>
    <EmptyState v-if="historyItems.length === 0 && !loading" text="暂无历史记录" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { HistoryItem } from '../types/history';
import { getHistory } from '../api/history';
import { getSceneLabel, getSceneColor } from '../utils/scene';
import { formatDate } from '../utils/format';
import EmptyState from './EmptyState.vue';

const router = useRouter();
const historyItems = ref<HistoryItem[]>([]);
const loading = ref(false);
const finished = ref(false);

const loadHistory = async () => {
  if (loading.value) return;
  
  loading.value = true;
  try {
    const history = await getHistory();
    historyItems.value = history;
    finished.value = true;
  } catch (error) {
    console.error('Load history error:', error);
  } finally {
    loading.value = false;
  }
};

const goToDetail = (imageId: number) => {
  router.push(`/history/${imageId}`);
};

const getImageUrl = (fileName: string) => {
  return `/uploads/${fileName}`;
};

onMounted(() => {
  loadHistory();
});
</script>

<style scoped>
.history-list {
  padding: 16px;
}

.history-item {
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.item-content {
  display: flex;
  padding: 12px;
}

.item-left {
  margin-right: 12px;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.item-right {
  flex: 1;
  min-width: 0;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-time {
  font-size: 12px;
  color: #999;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-actions {
  font-size: 12px;
  color: #999;
}
</style>
