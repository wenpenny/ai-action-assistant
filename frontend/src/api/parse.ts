import http from './http';
import type { Entities, ParseItem } from '../types/parse';

interface ParseUpdateRequest {
  items: ParseItem[];
}

interface ParseItemUpdateRequest {
  scene_type: string;
  summary: string;
  entities: Entities;
  suggested_actions: string[];
}

export const getParseResult = async (imageId: number): Promise<any> => {
  return http.get(`/parse/${imageId}`);
};

export const updateParseResult = async (imageId: number, data: ParseUpdateRequest): Promise<any> => {
  return http.put(`/parse/${imageId}`, data);
};

export const updateParseItem = async (itemId: string, data: ParseItemUpdateRequest): Promise<any> => {
  return http.put(`/parse/item/${itemId}`, data);
};