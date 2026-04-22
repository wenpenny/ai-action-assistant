import http from './http';

interface UploadResponse {
  image_id: number;
  image_url: string;
}

export const uploadImage = async (formData: FormData): Promise<UploadResponse> => {
  return http.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const parseImage = async (imageId: number): Promise<any> => {
  return http.post(`/parse/${imageId}`);
};