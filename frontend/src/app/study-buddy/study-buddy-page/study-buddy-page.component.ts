import { Component, OnInit } from '@angular/core';
import { StudyBuddyService } from 'src/app/study-buddy.service'; // adjust the path based on your structure

// Define an interface for chat messages
interface ChatMessage {
  sender: 'user' | 'bot';
  message: string;
}

@Component({
  selector: 'app-study-buddy-page',
  templateUrl: './study-buddy-page.component.html',
  styleUrls: ['./study-buddy-page.component.css']
})
export class StudyBuddyPageComponent implements OnInit {
  chatMessages: ChatMessage[] = [];

  constructor(private studyBuddyService: StudyBuddyService) {}

  ngOnInit(): void {
    // Optionally add a welcome message
    this.chatMessages.push({
      sender: 'bot',
      message: 'Welcome to Study Buddy! How can I help you today?'
    });
  }

  generatePracticeProblems(): void {
    const courseId = 'some-course-id'; // Replace with an actual course ID or get it from context
    this.studyBuddyService.getPracticeProblems(courseId).subscribe({
      next: (problems) => {
        // Format the dummy problems into a single message (you could format them better)
        const message = problems.map((p: any) => p.question_text).join('\n');
        this.chatMessages.push({ sender: 'bot', message });
      },
      error: (err) => {
        console.error('Error fetching practice problems', err);
        this.chatMessages.push({
          sender: 'bot',
          message: 'There was an error fetching practice problems.'
        });
      }
    });
  }

  generateStudyGuide(): void {
    const courseId = 'some-course-id'; // Replace as needed
    // For demonstration, let's assume you have a method in your service called generateStudyGuide.
    // If not, you could simulate a call to your backend.
    this.studyBuddyService
      .generateStudyGuide(courseId, ['topic1', 'topic2'])
      .subscribe({
        next: (guide) => {
          // Assume the guide has a "content" property
          this.chatMessages.push({ sender: 'bot', message: guide.content });
        },
        error: (err) => {
          console.error('Error generating study guide', err);
          this.chatMessages.push({
            sender: 'bot',
            message: 'There was an error generating the study guide.'
          });
        }
      });
  }
}
