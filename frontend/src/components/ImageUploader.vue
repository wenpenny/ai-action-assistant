<template>
  <div class="image-uploader">
    <div class="upload-wrapper" :class="{ 'is-dragover': isDragover, 'is-uploading': loading }">
      <van-uploader
        v-model="fileList"
        :after-read="handleAfterRead"
        :max-count="1"
        :disabled="loading"
        :preview-full-image="false"
        :multiple="false"
        :before-read="beforeRead"
        @drop.native="handleDrop"
        @dragover.native="handleDragover"
        @dragleave.native="handleDragleave"
      >
        <div class="upload-area" v-if="!loading">
          <div class="upload-icon-wrapper">
            <van-icon name="photo" size="36" class="upload-icon" />
            <div class="upload-icon-bg"></div>
          </div>
          <p class="upload-text">点击或拖拽上传截图</p>
          <p class="upload-hint">
            <van-icon name="shield-check" size="12" />
            支持 JPG、PNG、GIF 格式，最大 10MB
          </p>
          <div class="upload-features">
            <span class="feature-tag">
              <van-icon name="completed" size="12" />
              智能识别
            </span>
            <span class="feature-tag">
              <van-icon name="completed" size="12" />
              快速解析
            </span>
          </div>
        </div>
        <div class="upload-loading" v-else>
          <div class="loading-animation">
            <div class="loading-circle"></div>
            <van-icon name="photograph" size="40" class="loading-icon" />
          </div>
          <p class="loading-text">正在上传并分析...</p>
          <p class="loading-hint">请稍候</p>
        </div>
      </van-uploader>
    </div>
    <transition name="progress-fade">
      <van-progress
        v-if="loading"
        :percentage="uploadProgress"
        class="upload-progress"
        stroke-width="4"
        track-color="#e6e6e6"
        color="linear-gradient(90deg, #667eea 0%, #764ba2 100%)"
      />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { showToast } from 'vant';
import { uploadImage, parseImage } from '../api/upload';

const emit = defineEmits<{
  'upload-success': [imageId: number, imageUrl: string]
}>();

const fileList = ref<any[]>([]);
const loading = ref(false);
const uploadProgress = ref(0);
const isDragover = ref(false);

const beforeRead = (file: any) => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过 10MB');
    return false;
  }
  return true;
};

const handleDrop = () => {
  isDragover.value = false;
};

const handleDragover = () => {
  isDragover.value = true;
};

const handleDragleave = () => {
  isDragover.value = false;
};

const handleAfterRead = async (file: any) => {
  loading.value = true;
  uploadProgress.value = 0;
  
  try {
    const formData = new FormData();
    formData.append('file', file.file);
    
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10;
      }
    }, 200);
    
    const uploadResult = await uploadImage(formData);
    clearInterval(progressInterval);
    uploadProgress.value = 100;
    
    await parseImage(uploadResult.image_id);
    
    emit('upload-success', uploadResult.image_id, uploadResult.image_url);
  } catch (error) {
    showToast('上传失败，请重试');
    console.error('上传失败:', error);
  } finally {
    loading.value = false;
    uploadProgress.value = 0;
    fileList.value = [];
  }
};
</script>

<style scoped>
.image-uploader {
  margin-bottom: 20px;
}

.upload-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 4px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}

.upload-wrapper.is-dragover {
  transform: scale(1.02);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
}

.upload-wrapper.is-dragover .upload-area {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  border: 2px dashed #d9d9d9;
  border-radius: 16px;
  background-color: transparent;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.03) 0%, rgba(118, 75, 162, 0.03) 100%);
}

.upload-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.upload-icon {
  position: relative;
  z-index: 1;
  color: #667eea;
  transition: all 0.3s ease;
}

.upload-icon-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-radius: 50%;
  animation: pulse-icon 2s ease-in-out infinite;
}

@keyframes pulse-icon {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
    opacity: 0.7;
  }
}

.upload-text {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  letter-spacing: 0.5px;
}

.upload-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #999;
  margin: 0 0 20px 0;
}

.upload-features {
  display: flex;
  gap: 12px;
}

.feature-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #667eea;
  background: rgba(102, 126, 234, 0.08);
  padding: 6px 12px;
  border-radius: 20px;
}

.upload-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 24px;
}

.loading-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.loading-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

.loading-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #667eea;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.loading-text {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.loading-hint {
  margin: 0;
  font-size: 13px;
  color: #999;
}

.upload-progress {
  margin-top: 12px;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fade-enter-active,
.progress-fade-leave-active {
  transition: all 0.3s ease;
}

.progress-fade-enter-from,
.progress-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

:deep(.van-uploader__upload) {
  margin: 0;
}

:deep(.van-uploader__preview) {
  display: none;
}
</style>