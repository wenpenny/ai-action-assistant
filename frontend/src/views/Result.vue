<template>
  <div class="result">
    <div class="background-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
    </div>

    <van-nav-bar
      title="解析结果"
      left-text="返回"
      @click-left="goBack"
      class="nav-bar"
    />

    <div v-if="loading" class="loading-container">
      <LoadingBlock />
    </div>

    <div v-else-if="error" class="error-container">
      <van-empty description="加载失败" />
      <van-button type="primary" @click="loadData">重试</van-button>
    </div>

    <div v-else class="result-content" :class="{ 'animate-in': mounted }">
      <div class="image-card">
        <div class="image-wrapper">
          <img :src="imageUrl" :alt="`上传的图片 ${imageId}`" />
          <div class="image-overlay">
            <van-icon name="scan" size="24" />
          </div>
        </div>
        <div class="image-badge">
          <van-icon name="success" size="14" />
          已识别
        </div>
      </div>

      <div class="ocr-section" :class="{ 'animate-in': mounted }">
        <div class="section-header" @click="ocrCollapsed = !ocrCollapsed">
          <div class="section-title-wrapper">
            <van-icon name="records" size="20" />
            <span>OCR 识别结果</span>
          </div>
          <van-icon :name="ocrCollapsed ? 'arrow-down' : 'arrow-up'" size="16" />
        </div>
        <transition name="slide-fade">
          <div v-if="!ocrCollapsed" class="ocr-content">
            <div class="ocr-text">
              {{ parseResponse?.ocr_text || '无识别文本' }}
            </div>
          </div>
        </transition>
      </div>

      <div class="items-container" :class="{ 'animate-in': mounted }">
        <div class="section-header-main">
          <h2 class="section-title">
            <van-icon name="todo-list-o" size="22" />
            识别到的事项
          </h2>
          <span class="items-count" v-if="parseResponse?.items?.length">
            {{ parseResponse.items.length }} 项
          </span>
        </div>
        
        <div v-if="parseResponse?.items?.length === 0" class="empty-items">
          <van-empty description="未识别到事项" />
        </div>

        <div v-else class="items-list">
          <div 
            v-for="(item, index) in parseResponse?.items" 
            :key="item.item_id"
            class="item-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="item-header">
              <van-tag :color="getSceneColor(item.scene_type)" size="medium">
                {{ getSceneLabel(item.scene_type) }}
              </van-tag>
              <span class="item-id">ID: {{ item.item_id }}</span>
            </div>

            <div class="item-summary">
              {{ item.summary }}
            </div>

            <div class="item-entities">
              <div v-if="item.entities.title" class="entity-item">
                <div class="entity-icon">
                  <van-icon name="label-o" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">标题</span>
                  <span class="entity-value">{{ item.entities.title }}</span>
                </div>
              </div>
              <div v-if="item.entities.date || item.entities.deadline" class="entity-item">
                <div class="entity-icon">
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
                <div class="entity-icon">
                  <van-icon name="location-o" size="14" />
                </div>
                <div class="entity-content">
                  <span class="entity-label">地点</span>
                  <span class="entity-value">{{ item.entities.location || item.entities.address }}</span>
                </div>
              </div>
            </div>

            <div class="item-actions">
              <ActionButtons
                :action-plan="item.action_plan"
                :imageId="imageId"
                :itemId="item.item_id"
                @action-success="handleActionSuccess"
              />
            </div>

            <div class="item-footer">
              <van-button 
                size="small" 
                type="default" 
                @click="editItem(item)"
                icon="edit"
              >
                编辑
              </van-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <van-popup v-model:show="showEditPopup" position="bottom" round class="edit-popup-wrapper">
      <div class="edit-popup">
        <div class="edit-popup-header">
          <h3>编辑事项</h3>
          <van-icon name="cross" @click="showEditPopup = false" />
        </div>
        <EntityEditor
          :entities="editingItem?.entities || {}"
          :scene-type="editingItem?.scene_type"
          @save="updateItem"
          @cancel="showEditPopup = false"
        />
      </div>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { showToast, showConfirmDialog } from 'vant';
import LoadingBlock from '../components/LoadingBlock.vue';
import ActionButtons from '../components/ActionButtons.vue';
import EntityEditor from '../components/EntityEditor.vue';
import { getParseResult, updateParseItem } from '../api/parse';
import { getSceneLabel, getSceneColor } from '../utils/scene';
import type { ParseResponse, ParseItem } from '../types/parse';

const route = useRoute();
const router = useRouter();

const imageId = Number(route.params.id);
const loading = ref(true);
const error = ref(false);
const mounted = ref(false);
const parseResponse = ref<ParseResponse | null>(null);
const ocrCollapsed = ref(true);
const showEditPopup = ref(false);
const editingItem = ref<ParseItem | null>(null);

const imageUrl = computed(() => {
  return `/api/uploads/${imageId}.jpg`;
});

const loadData = async () => {
  loading.value = true;
  error.value = false;
  try {
    const result = await getParseResult(imageId);
    parseResponse.value = result;
    setTimeout(() => {
      mounted.value = true;
    }, 100);
  } catch (err) {
    console.error('加载解析结果失败:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const editItem = (item: ParseItem) => {
  editingItem.value = { ...item };
  showEditPopup.value = true;
};

const updateItem = async () => {
  if (!editingItem.value) return;
  
  try {
    await updateParseItem(editingItem.value.item_id, {
      scene_type: editingItem.value.scene_type,
      summary: editingItem.value.summary,
      entities: editingItem.value.entities,
      suggested_actions: editingItem.value.suggested_actions
    });
    showToast('更新成功');
    showEditPopup.value = false;
    loadData();
  } catch (err) {
    console.error('更新事项失败:', err);
    showToast('更新失败，请重试');
  }
};

const handleActionSuccess = (result: any) => {
  showToast(result.message || '动作执行成功');
};

const goBack = () => {
  router.push('/');
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.result {
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

.result-content {
  padding: 20px;
  position: relative;
  z-index: 1;
}

.result-content.animate-in .image-card {
  animation: slideInUp 0.5s ease forwards;
}

.result-content.animate-in .ocr-section {
  animation: slideInUp 0.5s ease 0.1s forwards;
  opacity: 0;
}

.result-content.animate-in .items-container {
  animation: slideInUp 0.5s ease 0.2s forwards;
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

.image-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  position: relative;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.item-footer {
  display: flex;
  justify-content: flex-end;
}

.edit-popup-wrapper {
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
}

.edit-popup {
  padding: 20px;
  max-height: 80vh;
  overflow-y: auto;
}

.edit-popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.edit-popup-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

@media (max-width: 480px) {
  .result-content {
    padding: 15px;
  }
  
  .item-card {
    padding: 16px;
  }
  
  .edit-popup {
    padding: 16px;
  }
  
  .section-title {
    font-size: 18px;
  }
}
</style>