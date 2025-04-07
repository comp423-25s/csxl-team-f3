export interface PracticeProblem {
  id: string;
  course_id: string;
  topic: string;
  difficulty: 'easy' | 'medium' | 'hard';
  question_type: 'multiple_choice' | 'free_response' | 'coding';
  question_text: string;
  answer: string;
  explanation: string;
  created_at: string;
  updated_at: string;
}

export interface StudySession {
  id: string;
  user_id: string;
  course_id: string;
  start_time: string;
  end_time: string | null;
  topics_covered: string[];
  problems_attempted: string[];
  score: number | null;
  feedback: string | null;
}

export interface StudentProgress {
  id: string;
  user_id: string;
  course_id: string;
  topic: string;
  proficiency_score: number;
  problems_attempted: number;
  problems_correct: number;
  last_updated: string;
}

export interface StudyGuide {
  id: string;
  course_id: string;
  topic: string;
  content: string;
  created_at: string;
  updated_at: string;
} 