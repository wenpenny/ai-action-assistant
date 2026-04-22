import http from './http';
import type { Entities } from '../types/parse';

interface ParseUpdateRequest {
  entities: Entities;
}

export const getParseResult = async (imageId: number): Promise<any> => {
  return http.get(`/parse/${imageId}`);
};

export const updateParseResult = async (imageId: number, data: ParseUpdateRequest): Promise<any> => {
  return http.put(`/parse/${imageId}`, data);
};