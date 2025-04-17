import { Component, OnInit } from '@angular/core';
import { StudyBuddyService } from 'src/app/study-buddy.service';
import { Course } from 'src/app/models/course.model';

@Component({
  selector: 'app-instructor-page',
  templateUrl: './instructor-page.component.html',
  styleUrls: ['./instructor-page.component.css']
})
export class InstructorPageComponent implements OnInit {
  courses: Course[] = [];
  selectedCourse: Course | null = null;
  report: string = '';

  constructor(private studyBuddyService: StudyBuddyService) {}

  ngOnInit(): void {
    this.studyBuddyService.getCourses().subscribe({
      next: (data) => (this.courses = data),
      error: (err) => console.error('Error loading courses', err)
    });
  }

  selectCourse(course: Course): void {
    this.selectedCourse = course;
    this.report = '';
  }

  generateReport(): void {
    if (!this.selectedCourse) return;
    this.studyBuddyService
      .generateInstructorReport(this.selectedCourse.id)
      .subscribe({
        next: (data) => (this.report = data.report),
        error: (err) => console.error('Error generating report', err)
      });
  }
}
