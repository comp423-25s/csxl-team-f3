from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, RootModel
from fastapi import Depends

from ...models.study_buddy.study_buddy_models import (
    PracticeProblem,
    StudyGuide,
    StudentProgress,
)
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


# 2) Your service:


class StudyBuddyService:
    def __init__(self, openai: OpenAIService = Depends()):
        self.openai = openai

    async def generate_practice_problems(
        self,
        course_id: str,
        course_description: str,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
        num_problems: int = 5,
    ) -> List[PracticeProblem]:
        """
        Generate practice problems using OpenAIService.
        """
        user_prompt = f"""
        Create {num_problems} practice problems for the following course:
        Course: {course_id} - {course_description}

        Topic: {topic if topic else 'Any relevant topic'}
        Difficulty: {difficulty if difficulty else 'Any difficulty'}
        Question Type: {question_type if question_type else 'Any type'}

        Each problem should:
        1. Test understanding of key concepts
        2. Be clear and unambiguous
        3. Include a detailed explanation of the correct answer
        4. Be appropriate for a computer science student
        5. Include relevant code examples if applicable

        Return a JSON object with this format:

            {{
            "problems": [
                {{
                "question_text": "The question text",
                "answer": "The correct answer",
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
                    course_id=UUID(course_id),
                    topic=topic or "General",
                    difficulty=difficulty or "medium",
                    question_type=question_type or "multiple_choice",
                    question_text=problem_data.question_text,
                    answer=problem_data.answer,
                    explanation=problem_data.explanation,
                )
            )
        return problems

    async def generate_study_guide(
        self,
        course_id: str,
        course_description: str,
        topics: List[str],
        student_progress: List[StudentProgress],
    ) -> StudyGuide:
        """
        Generate a personalized study guide using the OpenAIService.
        """
        weak_topics = [
            progress.topic
            for progress in student_progress
            if progress.proficiency_score < 0.7
        ]

        user_prompt = f"""
        Create a comprehensive study guide for this computer science course:
        Course: {course_id} - {course_description}

        Topics to cover:
        {', '.join(topics)}

        Focus especially on these weaker areas:
        {', '.join(weak_topics) if weak_topics else 'None identified'}

        The study guide should:
        1. Explain key concepts clearly and concisely
        2. Include relevant examples and code snippets
        3. Provide step-by-step explanations for complex topics
        4. Include common pitfalls and how to avoid them
        5. Suggest additional resources for further study
        6. Include practice exercises and solutions
        7. Use markdown formatting for better readability

        Return the guide in JSON like:
        {{
            "content": "# Title\\n ... (Markdown content)..."
        }}
        """

        system_prompt = (
            "You are an expert computer science tutor. "
            "Create detailed, well-structured study guides to help students master complex topics."
        )

        try:
            study_guide_resp: StudyGuideResponse = self.openai.prompt(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=StudyGuideResponse,
            )
        except Exception as e:
            raise Exception(f"Failed to generate study guide: {str(e)}")

        # Convert AI response to your domain model
        return StudyGuide(
            course_id=UUID(course_id),
            topic=", ".join(topics),
            content=study_guide_resp.content,
        )

    def calculate_proficiency_score(
        self, problems_attempted: int, problems_correct: int
    ) -> float:
        if problems_attempted == 0:
            return 0.0
        return problems_correct / problems_attempted
