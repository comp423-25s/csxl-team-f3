import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Course } from 'src/app/models/course.model';

export interface PracticeProblem {
  id: string;
  course_id: string;
  difficulty?: string;
  question_type?: string;
  question_text: string;
  answer: string;
  explanation: string;
}

export interface StudyGuide {
  id: string;
  course_id: string;
  content: string;
  created_at: string;
}

export interface InstructorReportResponse {
  report: string;
}

@Injectable({
  providedIn: 'root'
})
export class StudyBuddyService {
  constructor(private http: HttpClient) {}

  // Get list of courses from academics API
  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>('/api/academics/course');
  }

  // Generate practice problems for a given course
  getPracticeProblems(
    courseId: string,
    difficulty?: string,
    question_type?: string
  ): Observable<PracticeProblem[]> {
    let url = `/api/study-buddy/courses/${courseId}/practice-problems`;

    // Add query parameters if provided
    const params: any = {};
    if (difficulty) params.difficulty = difficulty;
    if (question_type) params.question_type = question_type;

    return this.http.get<PracticeProblem[]>(url, { params });
  }

  // Generate a study guide for a course
  generateStudyGuide(courseId: string): Observable<StudyGuide> {
    return this.http.post<StudyGuide>(
      `/api/study-buddy/courses/${courseId}/study-guide`,
      {}
    );
  }

  // Get instructor report
  getInstructorReport(courseId: string): Observable<InstructorReportResponse> {
    return this.http.get<InstructorReportResponse>(
      `/api/study-buddy/courses/${courseId}/instructor-report`
    );
  }
}
