<template>
  <div class="action-buttons">
    <div v-if="actions.length === 0" class="no-actions">
      <van-empty description="暂无建议动作" />
    </div>
    <div v-else class="button-grid">
      <van-button
        v-for="action in actions"
        :key="action"
        :type="getActionType(action)"
        :icon="getActionIcon(action)"
        block
        :loading="loadingActions.includes(action)"
        @click="handleExecuteAction(action)"
        class="action-button"
      >
        {{ getActionLabel(action) }}
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { showToast } from 'vant';
import { executeAction } from '../api/action';
import { getActionLabel, getActionIcon } from '../utils/actions';
import type { Entities } from '../types/parse';

const props = defineProps<{
  actions: string[]
  entities: Entities
  imageId: number
}>();

const emit = defineEmits<{
  'action-success': [result: any]
}>();

const loadingActions = ref<string[]>([]);

const getActionType = (action: string) => {
  const types: Record<string, any> = {
    create_todo: 'primary',
    set_reminder: 'warning',
    open_map: 'info',
    export_calendar: 'success'
  };
  return types[action] || 'default';
};

const handleExecuteAction = async (actionType: string) => {
  loadingActions.value.push(actionType);
  
  try {
    const payload = buildActionPayload(actionType, props.entities);
    const result = await executeAction(props.imageId, actionType, payload);
    
    emit('action-success', result);
    showToast(result.message || '动作执行成功');
    
    if (result.data?.map_url) {
      window.open(result.data.map_url, '_blank');
    }
    if (result.data?.ics_path) {
      window.open(result.data.ics_path, '_blank');
    }
  } catch (error) {
    showToast('动作执行失败，请重试');
    console.error('动作执行失败:', error);
  } finally {
    loadingActions.value = loadingActions.value.filter(action => action !== actionType);
  }
};

const buildActionPayload = (actionType: string, entities: Entities) => {
  switch (actionType) {
    case 'create_todo':
      return {
        title: entities.title || 'Untitled Todo',
        deadline: entities.deadline || entities.date
      };
    case 'set_reminder':
      return {
        title: entities.title || 'Untitled Reminder',
        remind_at: entities.deadline || `${entities.date} ${entities.start_time}`
      };
    case 'open_map':
      return {
        location: entities.location || entities.address
      };
    case 'export_calendar':
      return {
        title: entities.title || 'Untitled Event',
        date: entities.date,
        start_time: entities.start_time,
        end_time: entities.end_time,
        location: entities.location,
        description: `来自 AI 行动助手的日历事件`
      };
    default:
      return {};
  }
};
</script>

<style scoped>
.action-buttons {
  margin-bottom: 20px;
}

.button-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.action-button {
  margin-bottom: 0;
}

.no-actions {
  padding: 40px 0;
  text-align: center;
}
</style>