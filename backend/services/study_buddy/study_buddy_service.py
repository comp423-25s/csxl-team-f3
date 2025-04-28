from typing import List, Optional, Dict
from uuid import UUID
import json
from ...models.study_buddy.study_buddy_models import (
    PracticeProblem,
    StudyGuide,
)
from ...services.academics import CourseService
from pydantic import BaseModel
from fastapi import Depends

from ..openai import OpenAIService


# 1) Pydantic 2.x Root Models:


class PracticeProblemResponse(BaseModel):
    """Represents a single problem from the AI response."""

    question_text: str
    answer: str
    explanation: str


class PracticeProblemListResponse(BaseModel):
    """Represents a response containing a list of practice problems."""

    problems: List[PracticeProblemResponse]


class StudyGuideResponse(BaseModel):
    """Represents a study guide from the AI (could be raw markdown or structured JSON)."""

    content: str


class StudyBuddyService:
    def __init__(
        self,
        openai: OpenAIService = Depends(),
        course_service: CourseService = Depends(),
    ):
        self.openai = openai
        self.course_service = course_service

    async def generate_practice_problems(
        self,
        course_id: str,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
        num_problems: int = 5,
    ) -> List[PracticeProblem]:
        """
        Generate practice problems using OpenAI
        """
        # Get course details
        course = self.course_service.get_by_id(course_id)
        course_description = course.description

        user_prompt = f"""
        Create {num_problems} practice problems for the following course:
        Course: {course_id} - {course_description}
        
        Difficulty: {difficulty if difficulty else 'Any difficulty'}
        Question Type: {question_type if question_type else 'Any type'}
        
        Each problem should:
        1. Test understanding of key concepts
        2. Be clear and unambiguous
        3. Include a detailed explanation of the correct answer
        4. Be appropriate for a computer science student
        5. Include relevant code examples if applicable
        6. If the question is listed as multiple choice, provide the correct answer and the incorrect answers.
        
        
        Return a JSON object with this format:
        {{
            "problems": [
                {{
                "question_text": "The question text",
                "answer": "The correct answer (if multiple choice, provide the correct answer and the incorrect answers, clearly indicated as such)",
                "explanation": "Why it's correct"
                }}
            ]
        }}
        """

        system_prompt = (
            "You are an expert computer science educator. "
            "Generate high-quality practice problems that test conceptual understanding "
            "and practical skills."
        )

        try:
            response: PracticeProblemListResponse = self.openai.prompt(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=PracticeProblemListResponse,
            )
        except Exception as e:
            raise Exception(f"Failed to generate practice problems: {str(e)}")

        # Convert AI response to your domain model
        problems = []
        for problem_data in response.problems:
            problems.append(
                PracticeProblem(
                    course_id=course_id,
                    difficulty=difficulty,
                    question_type=question_type,
                    question_text=problem_data.question_text,
                    answer=problem_data.answer,
                    explanation=problem_data.explanation,
                )
            )
        return problems

    async def generate_study_guide(
        self,
        course_id: str,
    ) -> StudyGuide:
        """
        Generate a study guide using OpenAIService.
        This method constructs a prompt using the course description.
        """
        # Get course details
        course = self.course_service.get_by_id(course_id)
        course_description = course.description

        # Construct a prompt that requests a study guide
        user_prompt = f"""
        Create a comprehensive study guide for the following computer science course:
        Course: {course_id} - {course_description}
        
        The study guide should:
        1. Explain key concepts clearly and concisely.
        2. Include relevant examples and code snippets.
        3. Provide step-by-step explanations for complex topics.
        4. Highlight common pitfalls and suggest how to avoid them.
        5. Use markdown formatting for clear readability.
        
        Return a JSON object with the following format:
        {{
        "content": "# Study Guide Title\\n ... (Markdown content) ..."
        }}
        """

        # Provide a system prompt to set the role for the AI
        system_prompt = "You are an expert computer science tutor. Create a detailed and well-structured study guide to help students master complex topics."

        try:
            # Call the OpenAI service helper with our prompts, expecting a StudyGuideResponse
            study_guide_resp: StudyGuideResponse = self.openai.prompt(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=StudyGuideResponse,
            )
        except Exception as e:
            raise Exception(f"Failed to generate study guide: {str(e)}")

        # Build and return the StudyGuide object from the response.
        return StudyGuide(
            course_id=course_id,
            content=study_guide_resp.content,
        )

    async def generate_instructor_report(self, course_id: str) -> str:
        """
        Generate an instructor report for a course
        """
        # Get course details
        course = self.course_service.get_by_id(course_id)
        course_description = course.description

        system_prompt = (
            "You are an experienced CS instructor. "
            "Create a helpful teaching guide for this course."
        )
        user_prompt = f"""
        Create a teaching guide for the following course:
        Course: {course_id} - {course_description}
        
        The guide should focus on:
        1. Key concepts that students typically find challenging
        2. Recommended teaching approaches
        3. Suggested activities and exercises
        4. Common misconceptions and how to address them
        """
        response: StudyGuideResponse = self.openai.prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=StudyGuideResponse,
        )
        return response.content
