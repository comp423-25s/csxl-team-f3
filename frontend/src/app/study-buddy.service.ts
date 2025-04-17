import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Course } from 'src/app/models/course.model';

@Injectable({
  providedIn: 'root'
})
export class StudyBuddyService {
  private baseUrl = 'http://localhost:1560/api/study-buddy'; // adjust if needed

  constructor(private http: HttpClient) {}

  // Get list of courses
  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>(`${this.baseUrl}/courses`);
  }

  // Generate practice problems for a given course and topic
  getPracticeProblems(courseId: string, topic: string): Observable<any> {
    // If your backend expects query parameters, append them:
    return this.http.get<any>(
      `${this.baseUrl}/courses/${courseId}/practice-problems?topic=${topic}`
    );
  }

  // (Optional) Generate a study guide for a course on a specific topic
  generateStudyGuide(courseId: string, topics: string[]): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/study-guides`, {
      course_id: courseId,
      topics
    });
  }

  getInstructorStruggles(courseId: string) {
    return this.http.get<{ struggles: { [topic: string]: number } }>(
      `/api/study-buddy/instructor/data/${courseId}`
    );
  }

  generateInstructorReport(courseId: string) {
    return this.http.post<{ report: string }>(
      '/api/study-buddy/instructor/report',
      { course_id: courseId }
    );
  }
}
