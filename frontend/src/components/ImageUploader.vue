<template>
  <div class="image-uploader">
    <van-uploader
      v-model="fileList"
      :max-count="1"
      :after-read="afterRead"
      :before-read="beforeRead"
      :disabled="loading"
      accept="image/*"
      capture="camera"
      upload-text="点击上传截图"
    >
      <div class="uploader-content" v-if="fileList.length === 0">
        <van-icon name="photograph" size="48" color="#999" />
        <p class="uploader-text">点击或拖拽上传截图</p>
        <p class="uploader-hint">支持 JPG、PNG、GIF 等格式</p>
      </div>
    </van-uploader>
    <van-loading v-if="loading" class="loading" type="spinner" color="#1989fa" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { showToast } from 'vant';
import { uploadImage } from '../api/upload';
import { parseImage } from '../api/parse';
import { useRouter } from 'vue-router';

const router = useRouter();
const fileList = ref<any[]>([]);
const loading = ref(false);

const beforeRead = (file: File) => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过 10MB');
    return false;
  }
  return true;
};

const afterRead = async (file: any) => {
  loading.value = true;
  try {
    // 上传图片
    const uploadResponse = await uploadImage(file.file);
    // 解析图片
    await parseImage(uploadResponse.image_id);
    // 跳转到结果页
    router.push(`/result/${uploadResponse.image_id}`);
  } catch (error) {
    showToast('处理失败，请重试');
    console.error('Upload error:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.image-uploader {
  position: relative;
  margin: 20px 0;
}

.uploader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background-color: #fafafa;
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  transition: all 0.3s;
}

.uploader-content:hover {
  border-color: #1989fa;
  background-color: #f0f9ff;
}

.uploader-text {
  margin-top: 12px;
  font-size: 16px;
  color: #666;
}

.uploader-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
}
</style>
