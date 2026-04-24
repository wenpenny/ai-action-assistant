export interface Entities {
  title: string;
  date: string;
  start_time: string;
  end_time: string;
  deadline: string;
  location: string;
  address: string;
  link: string;
  task_name: string;
  required_materials: string[] | null;
  departure_time: string;
  departure_location: string;
  destination: string;
  hotel_name: string;
  booking_no: string;
}

export interface ActionPlanItem {
  action_type: string;
  label: string;
  payload: Record<string, any>;
  is_valid?: boolean;
}

export interface ParseItem {
  item_id: string;
  scene_type: 'schedule' | 'task' | 'travel' | 'other';
  summary: string;
  entities: Entities;
  suggested_actions: string[];
  action_plan: ActionPlanItem[];
}

export interface ParseResponse {
  image_id: number;
  ocr_text: string;
  items: ParseItem[];
}

export interface UploadResponse {
  image_id: number;
  image_url: string;
}

export interface ParseResult {
  scene_type: 'schedule' | 'task' | 'travel' | 'other';
  summary: string;
  entities: Entities;
  suggested_actions: string[];
}