export interface HistoryItem {
  image_id: number;
  file_name: string;
  file_path?: string;
  created_at: string;
  parse_status: string;
  item_count: number;
  action_count: number;
  scene_type?: string | null;
  summary?: string | null;
}

export interface ActionRecord {
  action_id: number;
  action_type: string;
  status: string;
  created_at: string;
}

export interface HistoryParseItem {
  item_id: string;
  scene_type: string;
  summary: string;
  entities: any;
  suggested_actions: string[];
  action_plan: any[];
  actions: ActionRecord[];
}

export interface HistoryDetail {
  image_id: number;
  file_name: string;
  image_url?: string;
  created_at: string;
  parse_status: string;
  ocr_text: string;
  items: HistoryParseItem[];
}