<template>
  <div class="result">
    <van-nav-bar 
      title="解析结果" 
      fixed 
      left-text="返回" 
      @click-left="goBack"
    />
    <div class="content">
      <LoadingBlock v-if="loading" text="正在解析..." />
      <div v-else-if="parseResult" class="result-content">
        <!-- 原图展示 -->
        <div class="image-container">
          <van-image :src="imageUrl" fit="contain" class="original-image" />
        </div>
        
        <!-- 解析摘要 -->
        <ParseSummaryCard :parse-result="parseResult" />
        
        <!-- 实体编辑器 -->
        <EntityEditor 
          :parse-result="parseResult" 
          :image-id="imageId" 
          @update:parse-result="updateParseResult"
        />
        
        <!-- 建议动作 -->
        <ActionButtons :parse-result="parseResult" :image-id="imageId" />
      </div>
      <EmptyState v-else text="解析失败，请重试" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { parseImage } from '../api/parse';
import { ParseResult } from '../types/parse';
import ParseSummaryCard from '../components/ParseSummaryCard.vue';
import EntityEditor from '../components/EntityEditor.vue';
import ActionButtons from '../components/ActionButtons.vue';
import LoadingBlock from '../components/LoadingBlock.vue';
import EmptyState from '../components/EmptyState.vue';

const route = useRoute();
const router = useRouter();
const imageId = computed(() => parseInt(route.params.id as string));
const parseResult = ref<ParseResult | null>(null);
const loading = ref(true);

const imageUrl = computed(() => {
  return `/uploads/${route.query.fileName || ''}`;
});

const loadParseResult = async () => {
  loading.value = true;
  try {
    const result = await parseImage(imageId.value);
    parseResult.value = result;
  } catch (error) {
    console.error('Load parse result error:', error);
    parseResult.value = null;
  } finally {
    loading.value = false;
  }
};

const updateParseResult = (result: ParseResult) => {
  parseResult.value = result;
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  loadParseResult();
});
</script>

<style scoped>
.result {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 60px;
  padding: 60px 16px 20px;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.image-container {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.original-image {
  max-height: 300px;
  border-radius: 4px;
}
</style>
