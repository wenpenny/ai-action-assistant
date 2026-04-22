<template>
  <div class="history-detail">
    <van-nav-bar
      title="历史详情"
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

    <div v-else class="detail-content">
      <div class="image-container">
        <img :src="historyData?.image?.file_path || ''" :alt="historyData?.image?.file_name || '历史图片'" />
      </div>

      <div class="info-section">
        <van-cell-group>
          <van-cell title="文件名" :value="historyData?.image?.file_name" />
          <van-cell title="上传时间" :value="formatDate(historyData?.image?.created_at || '')" />
          <van-cell v-if="historyData?.parse_result" title="场景类型" :value="getSceneLabel(historyData.parse_result.scene_type)" />
        </van-cell-group>
      </div>

      <div v-if="historyData?.parse_result" class="parse-section">
        <h3 class="section-title">解析结果</h3>
        <ParseSummaryCard :summary="historyData.parse_result.summary" />
        
        <div class="entities-section">
          <h4 class="subsection-title">结构化信息</h4>
          <van-cell-group>
            <van-cell v-if="historyData.parse_result.entities.title" title="标题" :value="historyData.parse_result.entities.title" />
            <van-cell v-if="historyData.parse_result.entities.date" title="日期" :value="historyData.parse_result.entities.date" />
            <van-cell v-if="historyData.parse_result.entities.start_time" title="开始时间" :value="historyData.parse_result.entities.start_time" />
            <van-cell v-if="historyData.parse_result.entities.end_time" title="结束时间" :value="historyData.parse_result.entities.end_time" />
            <van-cell v-if="historyData.parse_result.entities.deadline" title="截止时间" :value="historyData.parse_result.entities.deadline" />
            <van-cell v-if="historyData.parse_result.entities.location" title="地点" :value="historyData.parse_result.entities.location" />
            <van-cell v-if="historyData.parse_result.entities.address" title="地址" :value="historyData.parse_result.entities.address" />
            <van-cell v-if="historyData.parse_result.entities.link" title="链接" :value="historyData.parse_result.entities.link" is-link @click="openLink(historyData.parse_result.entities.link)" />
          </van-cell-group>
        </div>
      </div>

      <div v-if="historyData?.action_records && historyData.action_records.length > 0" class="action-section">
        <h3 class="section-title">动作记录</h3>
        <van-cell-group>
          <van-cell 
            v-for="record in historyData.action_records" 
            :key="record.id"
            :title="getActionLabel(record.action_type)"
            :value="formatDate(record.created_at)"
            is-link
          >
            <template #default>
              <div class="action-record">
                <div class="action-type">{{ getActionLabel(record.action_type) }}</div>
                <div class="action-status" :class="record.execute_status === 'success' ? 'success' : 'failed'">
                  {{ record.execute_status === 'success' ? '成功' : '失败' }}
                </div>
                <div class="action-time">{{ formatDate(record.created_at) }}</div>
              </div>
            </template>
          </van-cell>
        </van-cell-group>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import LoadingBlock from '../components/LoadingBlock.vue';
import ParseSummaryCard from '../components/ParseSummaryCard.vue';
import { getHistoryDetail } from '../api/history';
import { formatDate } from '../utils/format';
import { getSceneLabel } from '../utils/scene';
import { getActionLabel } from '../utils/actions';

const route = useRoute();
const router = useRouter();

const imageId = Number(route.params.id);
const loading = ref(true);
const error = ref(false);
const historyData = ref<any>(null);

const loadData = async () => {
  loading.value = true;
  error.value = false;
  try {
    const result = await getHistoryDetail(imageId);
    historyData.value = result;
  } catch (err) {
    console.error('加载历史详情失败:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const openLink = (link: string) => {
  if (link) {
    window.open(link, '_blank');
  }
};

const goBack = () => {
  router.push('/history');
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.history-detail {
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

.detail-content {
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

.info-section {
  margin-bottom: 20px;
}

.parse-section,
.action-section {
  margin-bottom: 20px;
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.subsection-title {
  font-size: 14px;
  font-weight: bold;
  margin: 16px 0 8px 0;
  color: #666;
}

.action-record {
  flex: 1;
  min-width: 0;
}

.action-type {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.action-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
  margin-bottom: 4px;
}

.action-status.success {
  background-color: #f6ffed;
  color: #52c41a;
}

.action-status.failed {
  background-color: #fff1f0;
  color: #ff4d4f;
}

.action-time {
  font-size: 12px;
  color: #999;
}

@media (max-width: 480px) {
  .detail-content {
    padding: 15px;
  }
}
</style>