export interface Entities {
  title: string | null;
  date: string | null;
  start_time: string | null;
  end_time: string | null;
  deadline: string | null;
  location: string | null;
  address: string | null;
  link: string | null;
  task_name: string | null;
  required_materials: string[] | null;
  departure_time: string | null;
  departure_location: string | null;
  destination: string | null;
  hotel_name: string | null;
  booking_no: string | null;
}

export interface ParseResult {
  scene_type: 'schedule' | 'task' | 'travel' | 'other';
  summary: string;
  entities: Entities;
  suggested_actions: string[];
}

export interface UploadResponse {
  image_id: number;
  image_url: string;
}
