export interface Course {
    id: string; // Use string to represent UUID (typically an ISO string)
    name: string;
    description: string;
    topics: string[];
    created_at: string;
    updated_at: string;
  }
  