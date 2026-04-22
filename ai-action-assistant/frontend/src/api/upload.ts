import http from './http';
import { UploadResponse } from '../types/parse';

export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  return http.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};
