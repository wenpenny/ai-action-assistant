<template>
  <van-card class="summary-card">
    <div class="card-header">
      <van-tag :color="sceneColor" size="small">{{ sceneLabel }}</van-tag>
      <span class="summary-title">{{ parseResult?.entities?.title || '未识别' }}</span>
    </div>
    <div class="card-content">
      <p class="summary-text">{{ parseResult?.summary }}</p>
      <div class="entity-info" v-if="parseResult?.entities">
        <div class="info-item" v-if="parseResult.entities.date">
          <van-icon name="calendar" size="16" />
          <span>{{ parseResult.entities.date }}</span>
        </div>
        <div class="info-item" v-if="parseResult.entities.start_time">
          <van-icon name="clock" size="16" />
          <span>{{ parseResult.entities.start_time }} {{ parseResult.entities.end_time ? `- ${parseResult.entities.end_time}` : '' }}</span>
        </div>
        <div class="info-item" v-if="parseResult.entities.location || parseResult.entities.address">
          <van-icon name="location" size="16" />
          <span>{{ parseResult.entities.location || parseResult.entities.address }}</span>
        </div>
        <div class="info-item" v-if="parseResult.entities.deadline">
          <van-icon name="time" size="16" />
          <span>截止日期: {{ parseResult.entities.deadline }}</span>
        </div>
      </div>
    </div>
  </van-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ParseResult } from '../types/parse';
import { getSceneLabel, getSceneColor } from '../utils/scene';

const props = defineProps<{
  parseResult: ParseResult | null;
}>();

const sceneLabel = computed(() => {
  return props.parseResult ? getSceneLabel(props.parseResult.scene_type) : '';
});

const sceneColor = computed(() => {
  return props.parseResult ? getSceneColor(props.parseResult.scene_type) : '#999999';
});
</script>

<style scoped>
.summary-card {
  margin: 16px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.summary-title {
  margin-left: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.card-content {
  padding-top: 0;
}

.summary-text {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 16px;
}

.entity-info {
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.info-item van-icon {
  margin-right: 8px;
  color: #999;
}
</style>
