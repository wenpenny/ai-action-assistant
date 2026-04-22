export interface ActionPayload {
  title?: string;
  deadline?: string;
  priority?: 'low' | 'medium' | 'high';
  remind_at?: string;
  address?: string;
  location?: string;
  start_time?: string;
  end_time?: string;
  description?: string;
}

export interface ActionRequest {
  image_id: number;
  action_type: 'create_todo' | 'set_reminder' | 'open_map' | 'export_calendar';
  payload: ActionPayload;
}

export interface ActionResponse {
  success: boolean;
  message: string;
  data: {
    todo_id?: number;
    reminder_id?: number;
    map_url?: string;
    calendar_url?: string;
  };
}
