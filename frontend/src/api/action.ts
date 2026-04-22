import http from './http';
import { ActionRequest, ActionResponse } from '../types/action';

export const executeAction = async (action: ActionRequest): Promise<ActionResponse> => {
  return http.post('/action/execute', action);
};
