<template>
  <div class="history-list">
    <div v-if="historyList.length === 0" class="empty">
      <van-empty description="暂无历史记录" />
    </div>
    <div v-else class="list">
      <van-cell
        v-for="item in historyList"
        :key="item.image_id"
        :title="item.file_name"
        :value="formatDate(item.created_at)"
        is-link
        @click="viewDetail(item.image_id)"
        class="history-item"
      >
        <template #icon>
          <div class="item-icon">
            <van-icon name="image" size="24" />
          </div>
        </template>
        <template #default>
          <div class="item-content">
            <div class="item-title">{{ item.file_name }}</div>
            <div class="item-meta">
              <van-tag v-if="item.scene_type" :color="getSceneColor(item.scene_type)">
                {{ getSceneLabel(item.scene_type) }}
              </van-tag>
              <span class="item-time">{{ formatDate(item.created_at) }}</span>
            </div>
            <div v-if="item.summary" class="item-summary">{{ item.summary }}</div>
          </div>
        </template>
      </van-cell>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '../utils/format';
import { getSceneLabel, getSceneColor } from '../utils/scene';

interface HistoryItem {
  image_id: number;
  file_name: string;
  file_path?: string;
  created_at: string;
  parse_status: string;
  scene_type?: string | null;
  summary?: string | null;
}

defineProps<{
  historyList: HistoryItem[]
}>();

const emit = defineEmits<{
  'view-detail': [imageId: number]
}>();

const viewDetail = (imageId: number) => {
  emit('view-detail', imageId);
};
</script>

<style scoped>
.history-list {
  margin-bottom: 20px;
}

.empty {
  padding: 40px 0;
  text-align: center;
}

.list {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.history-item {
  border-bottom: 1px solid #f0f0f0;
}

.history-item:last-child {
  border-bottom: none;
}

.item-icon {
  margin-right: 10px;
  color: #1890ff;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-meta {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.item-time {
  font-size: 12px;
  color: #999;
  margin-left: 10px;
}

.item-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  margin-top: 5px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>