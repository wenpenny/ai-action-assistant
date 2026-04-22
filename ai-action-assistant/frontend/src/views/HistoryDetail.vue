<template>
  <div class="history-detail">
    <van-nav-bar 
      title="历史详情" 
      fixed 
      left-text="返回" 
      @click-left="goBack"
    />
    <div class="content">
      <LoadingBlock v-if="loading" text="加载中..." />
      <div v-else-if="historyItem" class="detail-content">
        <!-- 原图展示 -->
        <div class="image-container">
          <van-image :src="imageUrl" fit="contain" class="original-image" />
          <div class="image-info">
            <span class="info-item">
              <van-icon name="clock" size="14" />
              {{ formatDate(historyItem.image.created_at) }}
            </span>
            <span class="info-item">
              <van-icon name="document" size="14" />
              {{ historyItem.image.file_name }}
            </span>
          </div>
        </div>
        
        <!-- 解析结果 -->
        <ParseSummaryCard v-if="historyItem.parse_result" :parse-result="parseResult" />
        <div v-else class="no-parse-result">
          <van-icon name="info-o" size="24" color="#999" />
          <span>无解析结果</span>
        </div>
        
        <!-- 动作记录 -->
        <van-card class="action-records">
          <template #title>
            执行记录 ({{ historyItem.action_records.length }})
          </template>
          <div v-if="historyItem.action_records.length > 0" class="records-list">
            <van-cell
              v-for="record in historyItem.action_records"
              :key="record.id"
              class="record-item"
            >
              <div class="record-content">
                <div class="record-header">
                  <span class="record-type">{{ getActionLabel(record.action_type) }}</span>
                  <van-tag 
                    :color="record.execute_status === 'success' ? '#52c41a' : '#ff4d4f'" 
                    size="small"
                  >
                    {{ record.execute_status === 'success' ? '成功' : '失败' }}
                  </van-tag>
                </div>
                <div class="record-time">{{ formatDate(record.created_at) }}</div>
                <div class="record-result" v-if="record.execute_result">
                  <pre>{{ JSON.stringify(record.execute_result, null, 2) }}</pre>
                </div>
              </div>
            </van-cell>
          </div>
          <div v-else class="empty-records">
            暂无执行记录
          </div>
        </van-card>
        
        <!-- 重新执行动作 -->
        <ActionButtons v-if="historyItem.parse_result" :parse-result="parseResult" :image-id="historyItem.image.id" />
      </div>
      <EmptyState v-else text="加载失败，请重试" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getHistoryById } from '../api/history';
import { HistoryItem } from '../types/history';
import { ParseResult } from '../types/parse';
import ParseSummaryCard from '../components/ParseSummaryCard.vue';
import ActionButtons from '../components/ActionButtons.vue';
import LoadingBlock from '../components/LoadingBlock.vue';
import EmptyState from '../components/EmptyState.vue';
import { getActionLabel } from '../utils/actions';
import { formatDate } from '../utils/format';

const route = useRoute();
const router = useRouter();
const imageId = computed(() => parseInt(route.params.id as string));
const historyItem = ref<HistoryItem | null>(null);
const loading = ref(true);

const parseResult = computed<ParseResult | null>(() => {
  if (!historyItem.value?.parse_result) return null;
  return {
    scene_type: historyItem.value.parse_result.scene_type,
    summary: historyItem.value.parse_result.summary,
    entities: historyItem.value.parse_result.entities,
    suggested_actions: historyItem.value.parse_result.suggested_actions
  };
});

const imageUrl = computed(() => {
  return `/uploads/${historyItem.value?.image.file_name || ''}`;
});

const loadHistoryDetail = async () => {
  loading.value = true;
  try {
    const result = await getHistoryById(imageId.value);
    historyItem.value = result;
  } catch (error) {
    console.error('Load history detail error:', error);
    historyItem.value = null;
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  loadHistoryDetail();
});
</script>

<style scoped>
.history-detail {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 60px;
  padding: 60px 16px 20px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.image-container {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.original-image {
  max-height: 300px;
  border-radius: 4px;
  margin-bottom: 12px;
}

.image-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-item van-icon {
  margin-right: 8px;
}

.no-parse-result {
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.no-parse-result van-icon {
  margin-right: 8px;
}

.action-records {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.records-list {
  padding-top: 8px;
}

.record-item {
  margin-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.record-content {
  padding: 8px 0;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.record-type {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.record-time {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.record-result {
  font-size: 12px;
  color: #666;
  background-color: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
  overflow-x: auto;
}

.record-result pre {
  margin: 0;
  white-space: pre-wrap;
}

.empty-records {
  text-align: center;
  padding: 20px 0;
  color: #999;
  font-size: 14px;
}
</style>
