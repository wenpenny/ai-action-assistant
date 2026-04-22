import http from './http';

export const getHistory = async (): Promise<any[]> => {
  return http.get('/history');
};

export const getHistoryDetail = async (imageId: number): Promise<any> => {
  return http.get(`/history/${imageId}`);
};