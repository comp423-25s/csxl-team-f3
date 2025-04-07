import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StudyBuddyService {
  getPracticeProblems(courseId: string): Observable<any> {
    return of([
      { question_text: 'What is polymorphism?' },
      { question_text: 'Explain inheritance in OOP.' }
    ]);
  }

  generateStudyGuide(courseId: string, topics: string[]): Observable<any> {
    return of({
      content: 'This is a dummy study guide for course ' + courseId + '.'
    });
  }
}
