export interface HistoryItem {
  image_id: number;
  file_name: string;
  file_path: string;
  created_at: string;
  parse_status: string;
  scene_type: string | null;
  summary: string | null;
}

export interface HistoryDetail {
  image: {
    image_id: number;
    file_name: string;
    file_path: string;
    created_at: string;
  };
  parse_result: {
    scene_type: string;
    summary: string;
    entities: any;
    suggested_actions: string[];
  } | null;
  action_records: any[];
}