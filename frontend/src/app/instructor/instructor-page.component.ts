import { Component, OnInit } from '@angular/core';
import {
  StudyBuddyService,
  InstructorReportResponse
} from 'src/app/study-buddy.service';
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
  loading = false;

  constructor(private studyBuddyService: StudyBuddyService) {}

  ngOnInit(): void {
    this.loadCourses();
  }

  loadCourses(): void {
    this.loading = true;
    this.studyBuddyService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Error loading courses', err);
        this.loading = false;
      }
    });
  }

  selectCourse(course: Course): void {
    this.selectedCourse = course;
    this.report = '';
  }

  generateReport(): void {
    if (!this.selectedCourse) return;

    this.loading = true;
    this.studyBuddyService
      .getInstructorReport(this.selectedCourse.id)
      .subscribe({
        next: (data: InstructorReportResponse) => {
          this.report = data.report;
          this.loading = false;
        },
        error: (err: any) => {
          console.error('Error generating report', err);
          this.loading = false;
        }
      });
  }
}
