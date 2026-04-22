import http from './http';
import { HistoryItem } from '../types/history';

export const getHistory = async (): Promise<HistoryItem[]> => {
  return http.get('/history');
};

export const getHistoryById = async (imageId: number): Promise<HistoryItem> => {
  return http.get(`/history/${imageId}`);
};
