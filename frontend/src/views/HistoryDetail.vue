<template>
  <div class="history-detail">
    <div class="background-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
    </div>

    <van-nav-bar title="历史详情" left-text="返回" @click-left="goBack" class="nav-bar" />

    <div v-if="loading" class="loading-container">
      <LoadingBlock />
    </div>

    <div v-else-if="error" class="error-container">
      <van-empty description="加载失败" />
      <van-button type="primary" @click="loadData">重试</van-button>
    </div>

    <div v-else class="detail-content" :class="{ 'animate-in': mounted }">
      <!-- 基本信息 -->
      <div class="info-card" :class="{ 'animate-in': mounted }">
        <div class="info-item">
          <div class="info-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <van-icon name="document-o" size="20" />
          </div>
          <div class="info-content">
            <div class="info-label">文件名</div>
            <div class="info-value">{{ historyData?.file_name }}</div>
          </div>
        </div>
        <div class="info-item">
          <div class="info-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <van-icon name="time-o" size="20" />
          </div>
          <div class="info-content">
            <div class="info-label">上传时间</div>
            <div class="info-value">{{ formatDate(historyData?.created_at || '') }}</div>
          </div>
        </div>
        <div class="info-item">
          <div class="info-icon" style="background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);">
            <van-icon name="success-o" size="20" />
          </div>
          <div class="info-content">
            <div class="info-label">解析状态</div>
            <div class="info-value">{{ historyData?.parse_status }}</div>
          </div>
        </div>
      </div>

      <!-- 图片预览 -->
      <div class="image-card" :class="{ 'animate-in': mounted }">
        <div class="image-wrapper">
          <img :src="imageUrl" :alt="historyData?.file_name || '历史图片'" @error="handleImageError" />
          <div v-if="imageError" class="image-error">
            <van-icon name="photo-fail" size="40" />
            <p>图片加载失败</p>
          </div>
          <div class="image-overlay">
            <van-icon name="scan" size="24" />
          </div>
        </div>
        <div class="image-badge">
          <van-icon name="history" size="14" />
          历史记录
        </div>
      </div>

      <!-- OCR 文本 -->
      <div class="ocr-section" :class="{ 'animate-in': mounted }">
        <div class="section-header" @click="ocrCollapsed = !ocrCollapsed">
          <div class="section-title-wrapper">
            <van-icon name="records" size="20" />
            <span>原始 OCR 文本</span>
          </div>
          <van-icon :name="ocrCollapsed ? 'arrow-down' : 'arrow-up'" size="16" />
        </div>
        <transition name="slide-fade">
          <div v-if="!ocrCollapsed" class="ocr-content">
            <div class="ocr-text">
              {{ historyData?.ocr_text || '无识别文本' }}
            </div>
          </div>
        </transition>
      </div>

      <!-- 事项列表 -->
      <div class="items-container" :class="{ 'animate-in': mounted }">
        <div class="section-header-main">
          <h2 class="section-title">
            <van-icon name="todo-list-o" size="22" />
            识别到的事项
          </h2>
          <span class="items-count" v-if="historyData?.items?.length">
            {{ historyData.items.length }} 项
          </span>
        </div>
        
        <div v-if="historyData?.items?.length === 0" class="empty-items">
          <van-empty description="未识别到事项" />
        </div>

        <div v-else class="items-list">
          <div v-for="(item, index) in historyData?.items" :key="item.item_id" class="item-card" :style="{ animationDelay: `${index * 0.1}s` }">
            <!-- 事项头部 -->
            <div class="item-header">
              <div class="header-left">
                <van-tag :color="getSceneColor(item.scene_type)" size="medium">
                  {{ getSceneLabel(item.scene_type) }}
                </van-tag>
                <span class="item-id">ID: {{ item.item_id }}</span>
              </div>
              <div class="header-right">
                <van-tag :type="getItemStatusType(item)">
                  {{ getItemStatusText(item) }}
                </van-tag>
              </div>
            </div>

            <!-- 事项摘要 -->
            <div class="item-summary">
              {{ item.summary }}
            </div>

            <!-- 关键实体 -->
            <div class="item-entities" v-if="hasEntities(item)">
              <div v-if="item.entities.title" class="entity-item">
                <div class="entity-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                  <van-icon name="label-o" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">标题</span>
                  <span class="entity-value">{{ item.entities.title }}</span>
                </div>
              </div>
              <div v-if="item.entities.date || item.entities.deadline" class="entity-item">
                <div class="entity-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                  <van-icon name="clock-o" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">时间</span>
                  <span class="entity-value">
                    {{ item.entities.date || item.entities.deadline }}
                    {{ item.entities.start_time ? ` ${item.entities.start_time}` : '' }}
                  </span>
                </div>
              </div>
              <div v-if="item.entities.location || item.entities.address" class="entity-item">
                <div class="entity-icon" style="background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);">
                  <van-icon name="location-o" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">地点</span>
                  <span class="entity-value">{{ item.entities.location || item.entities.address }}</span>
                </div>
              </div>
              <div v-if="item.entities.link" class="entity-item">
                <div class="entity-icon" style="background: linear-gradient(135deg, #faad14 0%, #ffc53d 100%);">
                  <van-icon name="link" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">链接</span>
                  <span class="entity-value">{{ item.entities.link }}</span>
                </div>
              </div>
              <div v-if="item.entities.required_materials && item.entities.required_materials.length > 0" class="entity-item">
                <div class="entity-icon" style="background: linear-gradient(135deg, #722ed1 0%, #b37feb 100%);">
                  <van-icon name="paperclip" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">材料</span>
                  <span class="entity-value">{{ item.entities.required_materials.join(', ') }}</span>
                </div>
              </div>
            </div>

            <!-- 动作记录 -->
            <div v-if="item.actions && item.actions.length > 0" class="item-actions">
              <div class="subsection-title">
                <van-icon name="history" size="16" />
                动作记录
              </div>
              <div class="action-timeline">
                <div v-for="action in item.actions" :key="action.action_id" class="action-timeline-item">
                  <div class="timeline-dot" :class="action.status === 'completed' ? 'success' : 'failed'"></div>
                  <div class="timeline-content">
                    <div class="action-type">{{ getActionLabel(action.action_type) }}</div>
                    <div class="action-status" :class="action.status === 'completed' ? 'success' : 'failed'">
                      {{ action.status === 'completed' ? '成功' : '失败' }}
                    </div>
                    <div class="action-time">{{ formatDate(action.created_at) }}</div>
                    <div v-if="action.status === 'failed'" class="action-retry">
                      <van-button size="small" type="default" @click="handleRetryAction(action, item)">
                        重新执行
                      </van-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="item-actions">
              <div class="subsection-title">
                <van-icon name="history" size="16" />
                动作记录
              </div>
              <div class="no-actions">
                暂无执行记录
              </div>
            </div>

            <!-- 未完成的动作 -->
            <div v-if="item.action_plan && item.action_plan.length > 0" class="item-pending-actions">
              <div class="subsection-title">
                <van-icon name="play-circle-o" size="16" />
                待执行动作
              </div>
              <ActionButtons :action-plan="item.action_plan" :imageId="imageId" :itemId="item.item_id" @action-success="handleActionSuccess" />
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
import { showToast } from 'vant';
import LoadingBlock from '../components/LoadingBlock.vue';
import ActionButtons from '../components/ActionButtons.vue';
import { getHistoryDetail } from '../api/history';
import { executeItemAction } from '../api/action';
import { formatDate } from '../utils/format';
import { getSceneLabel, getSceneColor } from '../utils/scene';
import { getActionLabel } from '../utils/actions';
import type { HistoryDetail } from '../types/history';

const route = useRoute();
const router = useRouter();

const imageId = Number(route.params.id);
const loading = ref(true);
const error = ref(false);
const mounted = ref(false);
const historyData = ref<HistoryDetail | null>(null);
const ocrCollapsed = ref(true);
const imageError = ref(false);

const imageUrl = computed(() => {
  const url = historyData.value?.image_url;
  if (url) {
    if (url.startsWith('/')) {
      return `http://127.0.0.1:8000${url}`;
    }
    return url;
  }
  //  fallback to old method
  const fallbackUrl = `/uploads/${imageId}.jpg`;
  if (fallbackUrl.startsWith('/')) {
    return `http://127.0.0.1:8000${fallbackUrl}`;
  }
  return fallbackUrl;
});

const handleImageError = () => {
  imageError.value = true;
};

const hasEntities = (item: any) => {
  const entities = item.entities;
  return entities.title || 
         entities.date || 
         entities.deadline || 
         entities.location || 
         entities.address || 
         entities.link || 
         (entities.required_materials && entities.required_materials.length > 0);
};

const getItemStatusType = (item: any) => {
  const validActionCount = item.action_plan?.filter((action: any) => action.is_valid).length || 0;
  const totalActionCount = item.action_plan?.length || 0;
  
  if (totalActionCount === 0) return 'default';
  if (validActionCount === 0) return 'danger';
  if (validActionCount === totalActionCount) return 'success';
  return 'warning';
};

const getItemStatusText = (item: any) => {
  const validActionCount = item.action_plan?.filter((action: any) => action.is_valid).length || 0;
  const totalActionCount = item.action_plan?.length || 0;
  
  if (totalActionCount === 0) return '未处理';
  if (validActionCount === 0) return '需补全';
  if (validActionCount === totalActionCount) return '已完成';
  return '部分完成';
};

const loadData = async () => {
  loading.value = true;
  error.value = false;
  imageError.value = false;
  try {
    const result = await getHistoryDetail(imageId);
    historyData.value = result;
    setTimeout(() => {
      mounted.value = true;
    }, 100);
  } catch (err) {
    console.error('加载历史详情失败:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const handleRetryAction = async (action: any, item: any) => {
  if (action.status === 'completed') {
    showToast('该动作已完成');
    return;
  }

  try {
    const result = await executeItemAction(
      imageId,
      item.item_id,
      action.action_type,
      action.payload
    );
    showToast(result.message || '动作执行成功');
    loadData();
  } catch (err) {
    console.error('重新执行动作失败:', err);
    showToast('动作执行失败，请重试');
  }
};

const handleActionSuccess = (result: any) => {
  showToast(result.message || '动作执行成功');
  loadData();
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
}

.orb-1 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
  top: -50px;
  right: -50px;
}

.orb-2 {
  width: 180px;
  height: 180px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: 100px;
  left: -60px;
}

.nav-bar {
  background: transparent;
  position: relative;
  z-index: 10;
}

:deep(.van-nav-bar) {
  background: transparent;
}

:deep(.van-nav-bar__title) {
  color: #ffffff;
  font-weight: 600;
}

:deep(.van-nav-bar__text) {
  color: #ffffff;
}

:deep(.van-nav-bar__arrow) {
  color: #ffffff;
}

.loading-container,
.error-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 1;
}

.error-container {
  gap: 20px;
}

.detail-content {
  max-width: 430px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
  z-index: 1;
}

.detail-content.animate-in .info-card {
  animation: slideInUp 0.5s ease forwards;
}

.detail-content.animate-in .image-card {
  animation: slideInUp 0.5s ease 0.1s forwards;
}

.detail-content.animate-in .ocr-section {
  animation: slideInUp 0.5s ease 0.2s forwards;
  opacity: 0;
}

.detail-content.animate-in .items-container {
  animation: slideInUp 0.5s ease 0.3s forwards;
  opacity: 0;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  opacity: 0;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  margin-right: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  line-height: 1.4;
}

.image-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  position: relative;
  opacity: 0;
}

.image-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  display: block;
}

.image-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #999;
  gap: 10px;
}

.image-error p {
  margin: 0;
  font-size: 14px;
}

.image-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-badge {
  position: absolute;
  top: 28px;
  left: 28px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.ocr-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  margin-bottom: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.section-header:hover {
  background: rgba(102, 126, 234, 0.05);
}

.section-title-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.section-title-wrapper .van-icon {
  color: #667eea;
}

.ocr-content {
  padding: 0 20px 20px;
}

.ocr-text {
  padding: 16px;
  line-height: 1.8;
  white-space: pre-wrap;
  color: #555;
  background: #f9f9f9;
  border-radius: 12px;
  font-size: 14px;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.items-container {
  margin-bottom: 20px;
}

.section-header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.section-title .van-icon {
  color: #ffffff;
}

.items-count {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.empty-items {
  background-color: white;
  padding: 40px 20px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.item-card {
  background-color: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  animation: slideInUp 0.5s ease forwards;
  opacity: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.item-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-id {
  font-size: 12px;
  color: #999;
}

.item-summary {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #333;
  line-height: 1.5;
}

.item-entities {
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  border-radius: 12px;
}

.entity-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
  font-size: 14px;
}

.entity-item:last-child {
  margin-bottom: 0;
}

.entity-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  margin-right: 12px;
  flex-shrink: 0;
}

.entity-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.entity-label {
  font-size: 12px;
  color: #888;
  margin-bottom: 2px;
}

.entity-value {
  color: #333;
  font-weight: 500;
  line-height: 1.4;
}

.item-actions {
  margin-bottom: 16px;
}

.item-pending-actions {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e8e8e8;
}

.subsection-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #666;
}

.subsection-title .van-icon {
  color: #667eea;
}

.action-timeline {
  position: relative;
  padding-left: 20px;
}

.action-timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e8e8e8;
}

.action-timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.action-timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -20px;
  top: 4px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #d9d9d9;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-dot.success {
  background: #52c41a;
}

.timeline-dot.failed {
  background: #ff4d4f;
}

.timeline-content {
  background: #f9f9f9;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.action-type {
  font-size: 14px;
  font-weight: 600;
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
  margin-bottom: 8px;
}

.action-retry {
  margin-top: 8px;
}

.no-actions {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  color: #999;
  font-size: 14px;
}

@media (max-width: 480px) {
  .detail-content {
    padding: 15px;
  }
  
  .item-card {
    padding: 16px;
  }
  
  .section-title {
    font-size: 18px;
  }
  
  .info-card {
    padding: 16px;
  }
  
  .info-item {
    margin-bottom: 12px;
  }
}
</style>