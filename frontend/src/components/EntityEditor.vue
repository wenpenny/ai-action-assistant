<template>
  <div class="entity-editor">
    <h3 class="editor-title">编辑事项</h3>
    <van-form @submit="handleSubmit">
      <van-field
        v-model="localEntities.title"
        label="标题"
        placeholder="请输入标题"
        :rules="[{ required: true, message: '请输入标题' }]"
      />
      <van-field
        v-model="localEntities.date"
        label="日期"
        placeholder="YYYY-MM-DD"
      />
      <van-field
        v-model="localEntities.start_time"
        label="开始时间"
        placeholder="HH:MM"
      />
      <van-field
        v-model="localEntities.end_time"
        label="结束时间"
        placeholder="HH:MM"
      />
      <van-field
        v-model="localEntities.deadline"
        label="截止时间"
        placeholder="YYYY-MM-DD HH:MM"
      />
      <van-field
        v-model="localEntities.location"
        label="地点"
        placeholder="请输入地点"
      />
      <van-field
        v-model="localEntities.address"
        label="地址"
        placeholder="请输入地址"
      />
      <van-field
        v-model="localEntities.link"
        label="链接"
        placeholder="请输入链接"
      />
      <div class="editor-actions">
        <van-button type="default" @click="emit('cancel')">取消</van-button>
        <van-button type="default" @click="resetForm">重置</van-button>
        <van-button type="primary" native-type="submit" :loading="loading">保存</van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
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
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.editor-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.editor-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  gap: 10px;
}

@media (max-width: 480px) {
  .editor-actions {
    flex-direction: column;
  }
  
  .editor-actions .van-button {
    width: 100%;
  }
}
</style>