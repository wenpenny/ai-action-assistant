<template>
  <van-card class="entity-editor">
    <template #title>
      <div class="card-title">
        <span>解析详情</span>
        <van-button 
          size="small" 
          type="primary" 
          :loading="saving" 
          @click="saveChanges"
        >
          保存修改
        </van-button>
      </div>
    </template>
    <div class="editor-content">
      <van-cell-group>
        <van-field
          v-model="editedEntities.title"
          label="标题"
          placeholder="请输入标题"
        />
        <van-field
          v-model="editedEntities.date"
          label="日期"
          placeholder="请输入日期，如：2026-04-28"
        />
        <van-field
          v-model="editedEntities.start_time"
          label="开始时间"
          placeholder="请输入开始时间，如：19:00"
        />
        <van-field
          v-model="editedEntities.end_time"
          label="结束时间"
          placeholder="请输入结束时间，如：20:30"
        />
        <van-field
          v-model="editedEntities.deadline"
          label="截止日期"
          placeholder="请输入截止日期，如：2026-04-30"
        />
        <van-field
          v-model="editedEntities.location"
          label="地点"
          placeholder="请输入地点"
        />
        <van-field
          v-model="editedEntities.address"
          label="地址"
          placeholder="请输入地址"
        />
        <van-field
          v-model="editedEntities.link"
          label="链接"
          placeholder="请输入链接"
        />
        <van-field
          v-model="editedEntities.task_name"
          label="任务名称"
          placeholder="请输入任务名称"
        />
        <van-field
          v-model="editedEntities.departure_time"
          label="出发时间"
          placeholder="请输入出发时间"
        />
        <van-field
          v-model="editedEntities.departure_location"
          label="出发地点"
          placeholder="请输入出发地点"
        />
        <van-field
          v-model="editedEntities.destination"
          label="目的地"
          placeholder="请输入目的地"
        />
        <van-field
          v-model="editedEntities.hotel_name"
          label="酒店名称"
          placeholder="请输入酒店名称"
        />
        <van-field
          v-model="editedEntities.booking_no"
          label="订单号"
          placeholder="请输入订单号"
        />
        <van-field
          v-model="requiredMaterialsText"
          label="所需材料"
          placeholder="请输入所需材料，用逗号分隔"
        />
      </van-cell-group>
    </div>
  </van-card>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { showToast } from 'vant';
import { ParseResult, Entities } from '../types/parse';
import { updateParseResult } from '../api/parse';

const props = defineProps<{
  parseResult: ParseResult | null;
  imageId: number;
}>();

const emit = defineEmits<{
  (e: 'update:parseResult', result: ParseResult): void;
}>();

const saving = ref(false);
const editedEntities = ref<Entities>({
  title: null,
  date: null,
  start_time: null,
  end_time: null,
  deadline: null,
  location: null,
  address: null,
  link: null,
  task_name: null,
  required_materials: null,
  departure_time: null,
  departure_location: null,
  destination: null,
  hotel_name: null,
  booking_no: null
});

const requiredMaterialsText = computed({
  get: () => {
    return editedEntities.value.required_materials?.join(', ') || '';
  },
  set: (value) => {
    if (value) {
      editedEntities.value.required_materials = value.split(',').map(item => item.trim()).filter(Boolean);
    } else {
      editedEntities.value.required_materials = null;
    }
  }
});

watch(
  () => props.parseResult,
  (newResult) => {
    if (newResult) {
      editedEntities.value = { ...newResult.entities };
    }
  },
  { immediate: true, deep: true }
);

const saveChanges = async () => {
  if (!props.parseResult) return;
  
  saving.value = true;
  try {
    const updatedResult = await updateParseResult(props.imageId, {
      ...props.parseResult,
      entities: editedEntities.value
    });
    emit('update:parseResult', updatedResult);
    showToast('保存成功');
  } catch (error) {
    showToast('保存失败，请重试');
    console.error('Save error:', error);
  } finally {
    saving.value = false;
  }
};
</script>

<style scoped>
.entity-editor {
  margin: 16px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
}

.editor-content {
  padding-top: 8px;
}

van-field {
  font-size: 14px;
}

van-field::v-deep .van-field__label {
  width: 80px;
}
</style>
