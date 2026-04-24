<template>
  <div class="history-detail">
    <van-nav-bar
      title="历史详情"
      left-text="返回"
      @click-left="goBack"
    />

    <div v-if="loading" class="loading-container">
      <LoadingBlock />
    </div>

    <div v-else-if="error" class="error-container">
      <van-empty description="加载失败" />
      <van-button type="primary" @click="loadData">重试</van-button>
    </div>

    <div v-else class="detail-content">
      <!-- 图片展示 -->
      <div class="image-container">
        <img :src="imageUrl" :alt="historyData?.file_name || '历史图片'" />
      </div>

      <!-- 基本信息 -->
      <div class="info-section">
        <van-cell-group>
          <van-cell title="文件名" :value="historyData?.file_name" />
          <van-cell title="上传时间" :value="formatDate(historyData?.created_at || '')" />
          <van-cell title="解析状态" :value="historyData?.parse_status" />
        </van-cell-group>
      </div>

      <!-- OCR 文本 -->
      <div class="ocr-section">
        <van-collapse v-model="ocrCollapsed">
          <van-collapse-item title="OCR 识别结果">
            <div class="ocr-text">
              {{ historyData?.ocr_text || '无识别文本' }}
            </div>
          </van-collapse-item>
        </van-collapse>
      </div>

      <!-- 事项列表 -->
      <div class="items-section">
        <h3 class="section-title">识别到的事项</h3>
        
        <div v-if="historyData?.items?.length === 0" class="empty-items">
          <van-empty description="未识别到事项" />
        </div>

        <div v-else class="items-list">
          <div 
            v-for="item in historyData?.items" 
            :key="item.item_id"
            class="item-card"
          >
            <!-- 事项头部 -->
            <div class="item-header">
              <van-tag :color="getSceneColor(item.scene_type)">
                {{ getSceneLabel(item.scene_type) }}
              </van-tag>
              <span class="item-id">ID: {{ item.item_id }}</span>
            </div>

            <!-- 事项摘要 -->
            <div class="item-summary">
              {{ item.summary }}
            </div>

            <!-- 关键实体 -->
            <div class="item-entities">
              <div v-if="item.entities.title" class="entity-item">
                <span class="entity-label">标题：</span>
                <span class="entity-value">{{ item.entities.title }}</span>
              </div>
              <div v-if="item.entities.date || item.entities.deadline" class="entity-item">
                <span class="entity-label">时间：</span>
                <span class="entity-value">
                  {{ item.entities.date || item.entities.deadline }}
                  {{ item.entities.start_time ? ` ${item.entities.start_time}` : '' }}
                </span>
              </div>
              <div v-if="item.entities.location || item.entities.address" class="entity-item">
                <span class="entity-label">地点：</span>
                <span class="entity-value">{{ item.entities.location || item.entities.address }}</span>
              </div>
            </div>

            <!-- 动作记录 -->
            <div v-if="item.actions && item.actions.length > 0" class="item-actions">
              <h4 class="subsection-title">动作记录</h4>
              <van-cell-group>
                <van-cell 
                  v-for="action in item.actions" 
                  :key="action.action_id"
                  is-link
                >
                  <template #default>
                    <div class="action-record">
                      <div class="action-type">{{ getActionLabel(action.action_type) }}</div>
                      <div class="action-status" :class="action.status === 'completed' ? 'success' : 'failed'">
                        {{ action.status === 'completed' ? '成功' : '失败' }}
                      </div>
                      <div class="action-time">{{ formatDate(action.created_at) }}</div>
                    </div>
                  </template>
                </van-cell>
              </van-cell-group>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import LoadingBlock from '../components/LoadingBlock.vue';
import { getHistoryDetail } from '../api/history';
import { formatDate } from '../utils/format';
import { getSceneLabel, getSceneColor } from '../utils/scene';
import { getActionLabel } from '../utils/actions';
import type { HistoryDetail } from '../types/history';

const route = useRoute();
const router = useRouter();

const imageId = Number(route.params.id);
const loading = ref(true);
const error = ref(false);
const historyData = ref<HistoryDetail | null>(null);
const ocrCollapsed = ref(true);

const imageUrl = computed(() => {
  return `/api/uploads/${imageId}.jpg`;
});

const loadData = async () => {
  loading.value = true;
  error.value = false;
  try {
    const result = await getHistoryDetail(imageId);
    historyData.value = result;
  } catch (err) {
    console.error('加载历史详情失败:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.push('/history');
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.history-detail {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.loading-container,
.error-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.error-container {
  gap: 20px;
}

.detail-content {
  padding: 20px;
}

.image-container {
  margin-bottom: 20px;
  text-align: center;
}

.image-container img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  object-fit: cover;
}

.info-section {
  margin-bottom: 20px;
}

.ocr-section {
  margin-bottom: 24px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.ocr-text {
  padding: 16px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: #333;
}

.items-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #333;
}

.empty-items {
  background-color: white;
  padding: 40px 20px;
  border-radius: 8px;
  text-align: center;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.item-card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-id {
  font-size: 12px;
  color: #999;
}

.item-summary {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
  color: #333;
  line-height: 1.4;
}

.item-entities {
  margin-bottom: 20px;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.entity-item {
  margin-bottom: 8px;
  font-size: 14px;
}

.entity-item:last-child {
  margin-bottom: 0;
}

.entity-label {
  color: #666;
  margin-right: 8px;
}

.entity-value {
  color: #333;
  font-weight: 500;
}

.item-actions {
  margin-top: 16px;
}

.subsection-title {
  font-size: 14px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #666;
}

.action-record {
  flex: 1;
  min-width: 0;
}

.action-type {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.action-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
  margin-bottom: 4px;
}

.action-status.success {
  background-color: #f6ffed;
  color: #52c41a;
}

.action-status.failed {
  background-color: #fff1f0;
  color: #ff4d4f;
}

.action-time {
  font-size: 12px;
  color: #999;
}

@media (max-width: 480px) {
  .detail-content {
    padding: 15px;
  }
  
  .item-card {
    padding: 16px;
  }
}
</style>