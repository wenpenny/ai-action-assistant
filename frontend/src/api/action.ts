import http from './http';

interface ActionRequest {
  image_id: number;
  action_type: string;
  payload: any;
}

export const executeAction = async (imageId: number, actionType: string, payload: any): Promise<any> => {
  const request: ActionRequest = {
    image_id: imageId,
    action_type: actionType,
    payload: payload
  };
  return http.post('/action/execute', request);
};