import { Component, OnInit } from '@angular/core';
import {
  StudyBuddyService,
  PracticeProblem,
  StudyGuide
} from 'src/app/study-buddy.service';
import { Course } from 'src/app/models/course.model';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-study-buddy-page',
  templateUrl: './study-buddy-page.component.html',
  styleUrls: ['./study-buddy-page.component.css']
})
export class StudyBuddyPageComponent implements OnInit {
  courses: Course[] = [];
  selectedCourse: Course | null = null;
  chatMessages: { sender: 'user' | 'bot'; message: string }[] = [];
  problemForm: FormGroup;
  loading = false;
  showingStudyGuide = false;

  constructor(
    private studyBuddyService: StudyBuddyService,
    private fb: FormBuilder
  ) {
    this.problemForm = this.fb.group({
      difficulty: ['medium'],
      question_type: ['multiple_choice']
    });
  }

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
      error: (err) => {
        console.error('Error loading courses', err);
        this.loading = false;
      }
    });
  }

  selectCourse(course: Course): void {
    this.selectedCourse = course;
    this.showingStudyGuide = false;
    // Clear prior messages:
    this.chatMessages = [
      {
        sender: 'bot',
        message: `Selected course: ${course.subject_code} ${course.number} - ${course.title}`
      }
    ];
  }

  generatePracticeProblems(): void {
    if (!this.selectedCourse) return;

    this.loading = true;
    this.showingStudyGuide = false;
    const { difficulty, question_type } = this.problemForm.value;

    this.chatMessages.push({
      sender: 'user',
      message: `Generating ${difficulty} ${question_type} practice problems for ${this.selectedCourse.subject_code} ${this.selectedCourse.number}`
    });

    this.studyBuddyService
      .getPracticeProblems(this.selectedCourse.id, difficulty, question_type)
      .subscribe({
        next: (problems: PracticeProblem[]) => {
          this.loading = false;
          // Format and display each problem
          if (problems && problems.length > 0) {
            problems.forEach((problem: PracticeProblem) => {
              this.chatMessages.push({
                sender: 'bot',
                message: `Question: ${problem.question_text}\n\nAnswer: ${problem.answer}\n\nExplanation: ${problem.explanation}`
              });
            });
          } else {
            this.chatMessages.push({
              sender: 'bot',
              message:
                'No practice problems were generated. Please try again with different parameters.'
            });
          }
        },
        error: (err) => {
          this.loading = false;
          console.error('Error generating practice problems', err);
          this.chatMessages.push({
            sender: 'bot',
            message:
              'Error generating practice problems. Please try again later.'
          });
        }
      });
  }

  generateStudyGuide(): void {
    if (!this.selectedCourse) return;

    this.loading = true;
    this.showingStudyGuide = true;
    this.chatMessages = [
      {
        sender: 'user',
        message: `Generating study guide for ${this.selectedCourse.subject_code} ${this.selectedCourse.number} - ${this.selectedCourse.title}`
      }
    ];

    this.studyBuddyService
      .generateStudyGuide(this.selectedCourse.id)
      .subscribe({
        next: (guide: StudyGuide) => {
          this.loading = false;
          this.chatMessages.push({
            sender: 'bot',
            message: guide.content
          });
        },
        error: (err) => {
          this.loading = false;
          console.error('Error generating study guide', err);
          this.chatMessages.push({
            sender: 'bot',
            message: 'Error generating study guide. Please try again later.'
          });
        }
      });
  }
}
