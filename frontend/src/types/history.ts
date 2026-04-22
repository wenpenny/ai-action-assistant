import { ParseResult } from './parse';

export interface ImageInfo {
  id: number;
  file_name: string;
  file_path: string;
  created_at: string;
  parse_status: string;
}

export interface ActionRecord {
  id: number;
  action_type: string;
  action_payload: any;
  execute_status: string;
  execute_result: any;
  created_at: string;
}

export interface HistoryItem {
  image: ImageInfo;
  parse_result?: ParseResult & {
    id: number;
    image_id: number;
    created_at: string;
    updated_at?: string;
  };
  action_records: ActionRecord[];
}
