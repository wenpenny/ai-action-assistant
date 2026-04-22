<template>
  <div class="image-uploader">
    <van-uploader
      v-model="fileList"
      :after-read="handleAfterRead"
      :max-count="1"
      :disabled="loading"
      :upload-text="loading ? '上传中...' : '点击上传截图'"
      :preview-full-image="false"
      :multiple="false"
    >
      <div class="upload-area">
        <van-icon name="camera" size="48" />
        <p class="upload-text">{{ loading ? '上传中...' : '点击或拖拽上传截图' }}</p>
        <p class="upload-hint">支持 JPG、PNG、GIF 格式</p>
      </div>
    </van-uploader>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { showToast } from 'vant';
import { uploadImage, parseImage } from '../api/upload';

const emit = defineEmits<{
  'upload-success': [imageId: number]
}>();

const fileList = ref<any[]>([]);
const loading = ref(false);

const handleAfterRead = async (file: any) => {
  loading.value = true;
  
  try {
    // 上传图片
    const formData = new FormData();
    formData.append('file', file.file);
    
    const uploadResult = await uploadImage(formData);
    
    // 上传成功后自动解析
    await parseImage(uploadResult.image_id);
    
    // 通知父组件上传成功
    emit('upload-success', uploadResult.image_id);
  } catch (error) {
    showToast('上传失败，请重试');
    console.error('上传失败:', error);
  } finally {
    loading.value = false;
    fileList.value = [];
  }
};
</script>

<style scoped>
.image-uploader {
  margin-bottom: 20px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  background-color: #fafafa;
  transition: all 0.3s;
}

.upload-area:hover {
  border-color: #1890ff;
  background-color: #e6f7ff;
}

.upload-text {
  margin: 10px 0 5px 0;
  font-size: 16px;
  color: #333;
}

.upload-hint {
  font-size: 12px;
  color: #999;
  margin: 0;
}
</style>