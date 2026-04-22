import http from './http';
import { ParseResult } from '../types/parse';

export const parseImage = async (imageId: number): Promise<ParseResult> => {
  return http.post(`/parse/${imageId}`);
};

export const updateParseResult = async (imageId: number, data: Partial<ParseResult>): Promise<ParseResult> => {
  return http.put(`/parse/${imageId}`, data);
};
