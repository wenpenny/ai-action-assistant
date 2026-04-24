<template>
  <div class="action-buttons">
    <div v-if="actionPlan.length === 0" class="no-actions">
      <van-empty description="暂无建议动作" />
    </div>
    <div v-else class="button-grid">
      <div v-for="(action, index) in actionPlan" :key="index" class="action-item">
        <van-button
          :type="getActionType(action.action_type)"
          :icon="getActionIcon(action.action_type)"
          block
          :loading="loadingActions.includes(action.action_type)"
          :disabled="!action.is_valid"
          @click="handleExecuteAction(action)"
          class="action-button"
          :class="{
            'action-button-disabled': !action.is_valid,
            'action-button-loading': loadingActions.includes(action.action_type),
            'action-button-executed': executedActions.includes(action.action_type)
          }"
        >
          {{ action.label }}
        </van-button>
        <div v-if="!action.is_valid" class="action-hint">
          {{ getActionHint(action) }}
        </div>
        <div v-if="executedActions.includes(action.action_type)" class="action-status">
          <van-icon name="success" size="14" />
          已完成
        </div>
        <div v-if="actionResults[action.action_type]" class="action-result">
          <div class="result-content">
            <div class="result-message">{{ actionResults[action.action_type].message }}</div>
            <div v-if="actionResults[action.action_type].map_url" class="result-link">
              <van-button size="small" type="primary" @click="openMap(actionResults[action.action_type].map_url)">
                打开地图
              </van-button>
            </div>
            <div v-if="actionResults[action.action_type].ics_file_path" class="result-link">
              <van-button size="small" type="success" @click="downloadCalendar(actionResults[action.action_type].ics_file_path)">
                下载日历
              </van-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { showToast } from 'vant';
import { executeItemAction } from '../api/action';
import { getActionIcon } from '../utils/actions';
import type { ActionPlanItem } from '../types/parse';

const props = defineProps<{
  actionPlan: ActionPlanItem[]
  imageId: number
  itemId: string
}>();

const emit = defineEmits<{
  'action-success': [result: any]
}>();

const loadingActions = ref<string[]>([]);
const executedActions = ref<string[]>([]);
const actionResults = reactive<Record<string, any>>({});

const getActionType = (actionType: string) => {
  const types: Record<string, any> = {
    create_todo: 'primary',
    set_reminder: 'warning',
    open_map: 'primary',
    export_calendar: 'success'
  };
  return types[actionType] || 'default';
};

const getActionHint = (action: ActionPlanItem) => {
  const hints: Record<string, string> = {
    create_todo: '缺少标题，请先编辑',
    set_reminder: '缺少提醒时间，请先编辑',
    open_map: '缺少地点信息，请先编辑',
    export_calendar: '缺少时间信息，请先编辑'
  };
  return hints[action.action_type] || '信息不完整，请先编辑';
};

const handleExecuteAction = async (action: ActionPlanItem) => {
  if (!action.is_valid) {
    showToast(getActionHint(action));
    return;
  }

  loadingActions.value.push(action.action_type);
  
  try {
    const result = await executeItemAction(
      props.imageId, 
      props.itemId, 
      action.action_type, 
      action.payload
    );
    
    executedActions.value.push(action.action_type);
    actionResults[action.action_type] = result.data || {};
    actionResults[action.action_type].message = result.message || '动作执行成功';
    
    emit('action-success', result);
    showToast(result.message || '动作执行成功');
    
  } catch (error) {
    showToast('动作执行失败，请重试');
    console.error('动作执行失败:', error);
  } finally {
    loadingActions.value = loadingActions.value.filter(actionType => actionType !== action.action_type);
  }
};

const openMap = (url: string) => {
  window.open(url, '_blank');
};

const downloadCalendar = (url: string) => {
  window.open(url, '_blank');
};
</script>

<style scoped>
.action-buttons {
  margin-bottom: 20px;
}

.button-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.action-item {
  position: relative;
  transition: transform 0.3s ease;
}

.action-item:hover {
  transform: translateY(-2px);
}

.action-button {
  margin-bottom: 8px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: none;
}

.action-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  z-index: 1;
  transition: all 0.3s ease;
}

.action-button:hover::before {
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.action-button-disabled {
  background: #f5f5f5 !important;
  color: #999 !important;
  border: 1px solid #e8e8e8 !important;
}

.action-button-loading {
  opacity: 0.8;
}

.action-button-executed {
  opacity: 0.8;
  background: #52c41a !important;
  color: white !important;
}

:deep(.van-button--primary) {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  border: none;
}

:deep(.van-button--warning) {
  background: linear-gradient(135deg, #faad14 0%, #d48806 100%);
  border: none;
}

:deep(.van-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

:deep(.van-button--success) {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  border: none;
}

.action-hint {
  font-size: 12px;
  color: #999;
  text-align: center;
  margin-top: 4px;
  line-height: 1.4;
  background: #f9f9f9;
  padding: 4px 8px;
  border-radius: 6px;
  border-left: 3px solid #faad14;
}

.action-status {
  position: absolute;
  top: -8px;
  right: -8px;
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 10px;
  display: flex;
  align-items: center;
  gap: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.action-result {
  margin-top: 12px;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 8px;
  border: 1px solid #e6f7ff;
  animation: fadeIn 0.3s ease;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-message {
  font-size: 12px;
  color: #1890ff;
  font-weight: 500;
}

.result-link {
  display: flex;
  justify-content: flex-start;
}

.result-link .van-button {
  border-radius: 6px;
  font-size: 12px;
  padding: 4px 12px;
}

.no-actions {
  padding: 40px 0;
  text-align: center;
  background: #f9f9f9;
  border-radius: 12px;
  margin: 16px 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 480px) {
  .button-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .action-button {
    padding: 12px 0;
  }
}
</style>