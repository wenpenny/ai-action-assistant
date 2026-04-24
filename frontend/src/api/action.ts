import http from './http';

interface ActionRequest {
  image_id: number;
  action_type: string;
  payload: any;
  item_id?: string;
}

interface ItemActionRequest {
  image_id: number;
  item_id: string;
  action_type: string;
  payload: any;
}

export const executeAction = async (imageId: number, actionType: string, payload: any, itemId?: string): Promise<any> => {
  const request: ActionRequest = {
    image_id: imageId,
    action_type: actionType,
    payload: payload,
    item_id: itemId
  };
  return http.post('/action/execute', request);
};

export const executeItemAction = async (imageId: number, itemId: string, actionType: string, payload: any): Promise<any> => {
  const request: ItemActionRequest = {
    image_id: imageId,
    item_id: itemId,
    action_type: actionType,
    payload: payload
  };
  return http.post('/action/execute-item', request);
};