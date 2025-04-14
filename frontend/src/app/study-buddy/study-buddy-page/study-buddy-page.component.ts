import { Component, OnInit } from '@angular/core';
import { StudyBuddyService } from 'src/app/study-buddy.service';
import { Course } from 'src/app/models/course.model';

@Component({
  selector: 'app-study-buddy-page',
  templateUrl: './study-buddy-page.component.html',
  styleUrls: ['./study-buddy-page.component.css']
})
export class StudyBuddyPageComponent implements OnInit {
  courses: Course[] = [];
  selectedCourse: Course | null = null;
  chatMessages: { sender: 'user' | 'bot'; message: string }[] = [];

  constructor(private studyBuddyService: StudyBuddyService) {}

  ngOnInit(): void {
    this.loadCourses();
  }

  loadCourses(): void {
    this.studyBuddyService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
      },
      error: (err) => console.error('Error loading courses', err)
    });
  }

  selectCourse(course: Course): void {
    this.selectedCourse = course;
    // Optionally clear prior messages:
    this.chatMessages = [
      { sender: 'bot', message: `Selected course: ${course.name}` }
    ];
  }

  generatePracticeProblems(topic: string): void {
    if (!this.selectedCourse) return;
    const courseId = this.selectedCourse.id; // or some unique identifier you use (e.g., "COMP401")
    this.studyBuddyService.getPracticeProblems(courseId, topic).subscribe({
      next: (problems) => {
        // Assume problems is an array and extract the question_text
        const message = problems.map((p: any) => p.question_text).join('\n');
        this.chatMessages.push({ sender: 'bot', message });
      },
      error: (err) => {
        console.error('Error generating practice problems', err);
        this.chatMessages.push({
          sender: 'bot',
          message: 'Error generating practice problem.'
        });
      }
    });
  }

  generateStudyGuide(topic: string): void {
    if (!this.selectedCourse) return;
    const courseId = this.selectedCourse.id;
    this.studyBuddyService.generateStudyGuide(courseId, [topic]).subscribe({
      next: (guide) => {
        this.chatMessages.push({ sender: 'bot', message: guide.content });
      },
      error: (err) => {
        console.error('Error generating study guide', err);
        this.chatMessages.push({
          sender: 'bot',
          message: 'Error generating study guide.'
        });
      }
    });
  }
}
