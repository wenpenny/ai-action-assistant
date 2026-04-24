<template>
  <div class="action-buttons">
    <div v-if="actionPlan.length === 0" class="no-actions">
      <van-empty description="暂无建议动作" />
    </div>
    <div v-else class="button-grid">
      <van-button
        v-for="(action, index) in actionPlan"
        :key="index"
        :type="getActionType(action.action_type)"
        :icon="getActionIcon(action.action_type)"
        block
        :loading="loadingActions.includes(action.action_type)"
        @click="handleExecuteAction(action)"
        class="action-button"
      >
        {{ action.label }}
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { showToast } from 'vant';
import { executeItemAction } from '../api/action';
import { getActionLabel, getActionIcon } from '../utils/actions';
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

const getActionType = (actionType: string) => {
  const types: Record<string, any> = {
    create_todo: 'primary',
    set_reminder: 'warning',
    open_map: 'info',
    export_calendar: 'success'
  };
  return types[actionType] || 'default';
};

const handleExecuteAction = async (action: ActionPlanItem) => {
  loadingActions.value.push(action.action_type);
  
  try {
    const result = await executeItemAction(
      props.imageId, 
      props.itemId, 
      action.action_type, 
      action.payload
    );
    
    emit('action-success', result);
    showToast(result.message || '动作执行成功');
    
    if (result.data?.map_url) {
      window.open(result.data.map_url, '_blank');
    }
    if (result.data?.ics_file_path) {
      window.open(result.data.ics_file_path, '_blank');
    }
  } catch (error) {
    showToast('动作执行失败，请重试');
    console.error('动作执行失败:', error);
  } finally {
    loadingActions.value = loadingActions.value.filter(actionType => actionType !== action.action_type);
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