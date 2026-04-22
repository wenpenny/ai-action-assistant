<template>
  <van-card class="action-buttons">
    <template #title>
      建议动作
    </template>
    <div class="buttons-container">
      <van-button
        v-for="action in parseResult?.suggested_actions || []"
        :key="action"
        :type="actionType === action ? 'primary' : 'default'"
        :loading="loading"
        :disabled="loading"
        class="action-button"
        @click="executeAction(action)"
      >
        <van-icon :name="getActionIcon(action)" slot="left" />
        {{ getActionLabel(action) }}
      </van-button>
      <div v-if="(parseResult?.suggested_actions || []).length === 0" class="empty-actions">
        暂无建议动作
      </div>
    </div>
    <div v-if="actionResult" class="action-result">
      <van-icon :name="actionResult.success ? 'success' : 'cross'" :color="actionResult.success ? '#52c41a' : '#ff4d4f'" />
      <span>{{ actionResult.message }}</span>
      <a v-if="actionResult.data.map_url" :href="actionResult.data.map_url" target="_blank" class="result-link">
        打开地图
      </a>
      <a v-if="actionResult.data.calendar_url" :href="actionResult.data.calendar_url" target="_blank" class="result-link">
        下载日历
      </a>
    </div>
  </van-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { showToast } from 'vant';
import { ParseResult } from '../types/parse';
import { ActionRequest, ActionResponse } from '../types/action';
import { executeAction as apiExecuteAction } from '../api/action';
import { getActionLabel, getActionIcon } from '../utils/actions';

const props = defineProps<{
  parseResult: ParseResult | null;
  imageId: number;
}>();

const loading = ref(false);
const actionType = ref<string | null>(null);
const actionResult = ref<ActionResponse | null>(null);

const executeAction = async (action: string) => {
  if (!props.parseResult) return;
  
  actionType.value = action;
  loading.value = true;
  actionResult.value = null;
  
  try {
    const payload = generateActionPayload(action);
    const request: ActionRequest = {
      image_id: props.imageId,
      action_type: action as any,
      payload
    };
    
    const result = await apiExecuteAction(request);
    actionResult.value = result;
    showToast(result.message);
  } catch (error) {
    showToast('执行失败，请重试');
    console.error('Action error:', error);
  } finally {
    loading.value = false;
    actionType.value = null;
  }
};

const generateActionPayload = (action: string) => {
  const payload: any = {};
  const entities = props.parseResult?.entities;
  
  if (!entities) return payload;
  
  switch (action) {
    case 'create_todo':
      payload.title = entities.title || entities.task_name || '未命名任务';
      payload.deadline = entities.deadline || (entities.date ? `${entities.date} ${entities.start_time || '00:00'}` : undefined);
      payload.priority = 'medium';
      break;
    case 'set_reminder':
      payload.title = entities.title || '提醒';
      payload.remind_at = entities.date ? `${entities.date} ${entities.start_time || '00:00'}` : undefined;
      break;
    case 'open_map':
      payload.address = entities.address;
      payload.location = entities.location;
      break;
    case 'export_calendar':
      payload.title = entities.title || '事件';
      payload.start_time = entities.date ? `${entities.date} ${entities.start_time || '00:00'}` : undefined;
      payload.end_time = entities.date && entities.end_time ? `${entities.date} ${entities.end_time}` : undefined;
      payload.location = entities.location;
      payload.description = props.parseResult?.summary;
      break;
  }
  
  return payload;
};
</script>

<style scoped>
.action-buttons {
  margin: 16px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.buttons-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding-top: 8px;
}

.action-button {
  flex: 1;
  min-width: 120px;
}

.empty-actions {
  text-align: center;
  padding: 20px 0;
  color: #999;
  font-size: 14px;
}

.action-result {
  margin-top: 16px;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 6px;
  display: flex;
  align-items: center;
  font-size: 14px;
}

.action-result van-icon {
  margin-right: 8px;
}

.result-link {
  margin-left: 12px;
  color: #1989fa;
  text-decoration: none;
}

.result-link:hover {
  text-decoration: underline;
}
</style>
