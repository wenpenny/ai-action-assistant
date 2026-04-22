<template>
  <div class="result">
    <van-nav-bar
      title="解析结果"
      left-text="返回"
      @click-left="goBack"
    />

    <div v-if="loading" class="loading-container">
      <LoadingBlock />
    </div>

    <div v-else-if="error" class="error-container">
      <van-empty description="加载失败" />
      <van-button type="primary" @click="loadData">重试</van-button>
    </div>

    <div v-else class="result-content">
      <div class="image-container">
        <img :src="imageUrl" :alt="parseResult?.entities?.title || '上传的图片'" />
      </div>

      <div v-if="parseResult?.scene_type" class="scene-type">
        <van-tag :color="getSceneColor(parseResult.scene_type)">
          {{ getSceneLabel(parseResult.scene_type) }}
        </van-tag>
      </div>

      <ParseSummaryCard :summary="parseResult?.summary || ''" />

      <EntityEditor
        v-model:entities="entities"
        @save="updateEntities"
      />

      <ActionButtons
        :actions="parseResult?.suggested_actions || []"
        :entities="entities"
        :imageId="imageId"
        @action-success="handleActionSuccess"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { showToast } from 'vant';
import LoadingBlock from '../components/LoadingBlock.vue';
import ParseSummaryCard from '../components/ParseSummaryCard.vue';
import EntityEditor from '../components/EntityEditor.vue';
import ActionButtons from '../components/ActionButtons.vue';
import { getParseResult, updateParseResult } from '../api/parse';
import { getSceneLabel, getSceneColor } from '../utils/scene';
import type { Entities } from '../types/parse';

const route = useRoute();
const router = useRouter();

const imageId = Number(route.params.id);
const loading = ref(true);
const error = ref(false);
const parseResult = ref<any>(null);
const entities = ref<Entities>({
  title: '',
  date: '',
  start_time: '',
  end_time: '',
  deadline: '',
  location: '',
  address: '',
  link: '',
  task_name: '',
  required_materials: null,
  departure_time: '',
  departure_location: '',
  destination: '',
  hotel_name: '',
  booking_no: ''
});

const imageUrl = computed(() => {
  return parseResult.value?.image_url || '';
});

const loadData = async () => {
  loading.value = true;
  error.value = false;
  try {
    const result = await getParseResult(imageId);
    parseResult.value = result;
    if (result.entities) {
      entities.value = {
        title: result.entities.title || '',
        date: result.entities.date || '',
        start_time: result.entities.start_time || '',
        end_time: result.entities.end_time || '',
        deadline: result.entities.deadline || '',
        location: result.entities.location || '',
        address: result.entities.address || '',
        link: result.entities.link || '',
        task_name: result.entities.task_name || '',
        required_materials: result.entities.required_materials || null,
        departure_time: result.entities.departure_time || '',
        departure_location: result.entities.departure_location || '',
        destination: result.entities.destination || '',
        hotel_name: result.entities.hotel_name || '',
        booking_no: result.entities.booking_no || ''
      };
    }
  } catch (err) {
    console.error('加载解析结果失败:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const updateEntities = async (updatedEntities: Entities) => {
  try {
    await updateParseResult(imageId, { entities: updatedEntities });
    showToast('更新成功');
  } catch (err) {
    console.error('更新解析结果失败:', err);
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
  background-color: #f5f5f5;
}

.loading-container,
.error-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.error-container {
  gap: 20px;
}

.result-content {
  padding: 20px;
}

.image-container {
  margin-bottom: 20px;
  text-align: center;
}

.image-container img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  object-fit: cover;
}

.scene-type {
  margin-bottom: 16px;
}

@media (max-width: 480px) {
  .result-content {
    padding: 15px;
  }
}
</style>