<template>
  <div class="entity-editor">
    <van-form @submit="handleSubmit" class="editor-form">
      <!-- 基础信息 -->
      <div class="field-group">
        <div class="field-group-title">
          <van-icon name="info-o" size="16" />
          基础信息
        </div>
        <van-field
          v-model="localEntities.title"
          label="标题"
          placeholder="请输入标题"
          :rules="[{ required: true, message: '请输入标题' }]"
          class="field-item"
        />
        <van-field
          v-model="localEntities.task_name"
          label="任务名"
          placeholder="请输入任务名"
          class="field-item"
        />
      </div>

      <!-- 时间信息 -->
      <div class="field-group">
        <div class="field-group-title">
          <van-icon name="clock-o" size="16" />
          时间信息
        </div>
        <van-field
          v-model="localEntities.date"
          label="日期"
          placeholder="YYYY-MM-DD"
          class="field-item"
        />
        <van-field
          v-model="localEntities.start_time"
          label="开始时间"
          placeholder="HH:MM"
          class="field-item"
        />
        <van-field
          v-model="localEntities.end_time"
          label="结束时间"
          placeholder="HH:MM"
          class="field-item"
        />
        <van-field
          v-model="localEntities.deadline"
          label="截止时间"
          placeholder="YYYY-MM-DD HH:MM"
          class="field-item"
        />
      </div>

      <!-- 地点与链接 -->
      <div class="field-group">
        <div class="field-group-title">
          <van-icon name="location-o" size="16" />
          地点与链接
        </div>
        <van-field
          v-model="localEntities.location"
          label="地点"
          placeholder="请输入地点"
          class="field-item"
        />
        <van-field
          v-model="localEntities.address"
          label="地址"
          placeholder="请输入详细地址"
          class="field-item"
        />
        <van-field
          v-model="localEntities.link"
          label="链接"
          placeholder="请输入相关链接"
          class="field-item"
        />
      </div>

      <!-- 任务信息 -->
      <div class="field-group">
        <div class="field-group-title">
          <van-icon name="todo-list-o" size="16" />
          任务信息
        </div>
        <van-field
          v-model="materialsText"
          label="材料清单"
          placeholder="请输入材料，多个材料用逗号分隔"
          class="field-item"
        />
      </div>

      <!-- 旅行信息 (仅当场景类型为travel时显示) -->
      <div v-if="props.sceneType === 'travel'" class="field-group">
        <div class="field-group-title">
          <van-icon name="navigate" size="16" />
          旅行信息
        </div>
        <van-field
          v-model="localEntities.departure_time"
          label="出发时间"
          placeholder="YYYY-MM-DD HH:MM"
          class="field-item"
        />
        <van-field
          v-model="localEntities.departure_location"
          label="出发地点"
          placeholder="请输入出发地点"
          class="field-item"
        />
        <van-field
          v-model="localEntities.destination"
          label="目的地"
          placeholder="请输入目的地"
          class="field-item"
        />
        <van-field
          v-model="localEntities.hotel_name"
          label="酒店名称"
          placeholder="请输入酒店名称"
          class="field-item"
        />
        <van-field
          v-model="localEntities.booking_no"
          label="预订号"
          placeholder="请输入预订号"
          class="field-item"
        />
      </div>

      <!-- 操作按钮 -->
      <div class="editor-actions">
        <van-button type="default" @click="emit('cancel')" class="action-button cancel-button">
          取消
        </van-button>
        <van-button type="default" @click="resetForm" class="action-button reset-button">
          重置
        </van-button>
        <van-button type="primary" native-type="submit" :loading="loading" class="action-button save-button">
          保存
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { showToast } from 'vant';
import type { Entities } from '../types/parse';

const props = defineProps<{
  entities: Entities
  sceneType?: string
}>();

const emit = defineEmits<{
  'update:entities': [entities: Entities]
  'save': [entities: Entities]
  'cancel': []
}>();

const loading = ref(false);
const localEntities = ref<Entities>({
  title: props.entities.title || '',
  date: props.entities.date || '',
  start_time: props.entities.start_time || '',
  end_time: props.entities.end_time || '',
  deadline: props.entities.deadline || '',
  location: props.entities.location || '',
  address: props.entities.address || '',
  link: props.entities.link || '',
  task_name: props.entities.task_name || '',
  required_materials: props.entities.required_materials || null,
  departure_time: props.entities.departure_time || '',
  departure_location: props.entities.departure_location || '',
  destination: props.entities.destination || '',
  hotel_name: props.entities.hotel_name || '',
  booking_no: props.entities.booking_no || ''
});

// 材料清单文本，用于输入框
const materialsText = computed({
  get: () => {
    return localEntities.value.required_materials?.join(', ') || '';
  },
  set: (value) => {
    localEntities.value.required_materials = value
      ? value.split(',').map(item => item.trim()).filter(Boolean)
      : null;
  }
});

watch(() => props.entities, (newEntities) => {
  localEntities.value = {
    title: newEntities.title || '',
    date: newEntities.date || '',
    start_time: newEntities.start_time || '',
    end_time: newEntities.end_time || '',
    deadline: newEntities.deadline || '',
    location: newEntities.location || '',
    address: newEntities.address || '',
    link: newEntities.link || '',
    task_name: newEntities.task_name || '',
    required_materials: newEntities.required_materials || null,
    departure_time: newEntities.departure_time || '',
    departure_location: newEntities.departure_location || '',
    destination: newEntities.destination || '',
    hotel_name: newEntities.hotel_name || '',
    booking_no: newEntities.booking_no || ''
  };
}, { deep: true });

const handleSubmit = async () => {
  loading.value = true;
  try {
    emit('update:entities', localEntities.value);
    emit('save', localEntities.value);
    showToast('保存成功');
  } catch (error) {
    showToast('保存失败，请重试');
    console.error('保存失败:', error);
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  localEntities.value = {
    title: props.entities.title || '',
    date: props.entities.date || '',
    start_time: props.entities.start_time || '',
    end_time: props.entities.end_time || '',
    deadline: props.entities.deadline || '',
    location: props.entities.location || '',
    address: props.entities.address || '',
    link: props.entities.link || '',
    task_name: props.entities.task_name || '',
    required_materials: props.entities.required_materials || null,
    departure_time: props.entities.departure_time || '',
    departure_location: props.entities.departure_location || '',
    destination: props.entities.destination || '',
    hotel_name: props.entities.hotel_name || '',
    booking_no: props.entities.booking_no || ''
  };
};
</script>

<style scoped>
.entity-editor {
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  border-radius: 16px;
  padding: 0;
  overflow: hidden;
}

.editor-form {
  padding: 20px;
}

.field-group {
  margin-bottom: 24px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.field-group:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.field-group-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e6f7ff;
}

.field-item {
  margin-bottom: 12px;
}

.field-item:last-child {
  margin-bottom: 0;
}

:deep(.van-field) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.van-field__control) {
  border-radius: 0 8px 8px 0;
}

:deep(.van-field__label) {
  font-weight: 500;
  color: #666;
}

.editor-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #e8e8e8;
}

.action-button {
  flex: 1;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 12px 0;
  position: relative;
  overflow: hidden;
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

.cancel-button {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #e8e8e8;
}

.reset-button {
  background: #f0f9ff;
  color: #1890ff;
  border: 1px solid #e6f7ff;
}

.save-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .editor-form {
    padding: 16px;
  }
  
  .field-group {
    padding: 12px;
  }
  
  .editor-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .action-button {
    width: 100%;
  }
  
  .field-item {
    margin-bottom: 8px;
  }
}
</style>