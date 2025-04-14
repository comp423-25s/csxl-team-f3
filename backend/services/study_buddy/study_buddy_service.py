from typing import List, Optional, Dict, Any
from uuid import UUID
import openai
import os
import json
from ...models.study_buddy.study_buddy_models import (
    PracticeProblem,
    StudyGuide,
    StudentProgress,
)


class StudyBuddyService:
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv("UNC_OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = openai.OpenAI(api_key=api_key)

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
        Generate practice problems using OpenAI
        """
        prompt = f"""
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
        
        Format the response as a JSON array with the following structure for each problem:
        {{
            "question_text": "The question text",
            "answer": "The correct answer",
            "explanation": "Detailed explanation of why this is the correct answer"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert computer science educator. Generate high-quality practice problems that test conceptual understanding and practical skills.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Failed to generate practice problems")

            try:
                problems_data = json.loads(content)
                if not isinstance(problems_data, list):
                    problems_data = [problems_data]
            except json.JSONDecodeError:
                raise ValueError("Failed to parse practice problems response")

            problems = []
            for problem_data in problems_data:
                if not isinstance(problem_data, dict):
                    continue

                problems.append(
                    PracticeProblem(
                        course_id=UUID(course_id),
                        topic=topic or "General",
                        difficulty=difficulty or "medium",
                        question_type=question_type or "multiple_choice",
                        question_text=problem_data.get("question_text", ""),
                        answer=problem_data.get("answer", ""),
                        explanation=problem_data.get("explanation", ""),
                    )
                )

            return problems

        except Exception as e:
            raise Exception(f"Failed to generate practice problems: {str(e)}")

    async def generate_study_guide(
        self,
        course_id: str,
        course_description: str,
        topics: List[str],
        student_progress: List[StudentProgress],
    ) -> StudyGuide:
        """
        Generate a personalized study guide using OpenAI
        """
        # Identify weak areas based on student progress
        weak_topics = [
            progress.topic
            for progress in student_progress
            if progress.proficiency_score < 0.7
        ]

        # Create prompt for OpenAI
        prompt = f"""
        Create a comprehensive study guide for the following computer science course:
        Course: {course_id} - {course_description}
        
        Topics to cover:
        {', '.join(topics)}
        
        Focus especially on these areas where the student needs improvement:
        {', '.join(weak_topics) if weak_topics else 'None identified'}
        
        The study guide should:
        1. Explain key concepts clearly and concisely
        2. Include relevant examples and code snippets
        3. Provide step-by-step explanations for complex topics
        4. Include common pitfalls and how to avoid them
        5. Suggest additional resources for further study
        6. Include practice exercises and solutions
        7. Use markdown formatting for better readability
        
        Format the study guide in markdown with clear sections and subsections.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert computer science tutor. Create detailed, well-structured study guides that help students master complex topics.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Failed to generate study guide")

            return StudyGuide(
                course_id=UUID(course_id),
                topic=", ".join(topics),
                content=content,
            )

        except Exception as e:
            raise Exception(f"Failed to generate study guide: {str(e)}")

    def calculate_proficiency_score(
        self, problems_attempted: int, problems_correct: int
    ) -> float:
        """
        Calculate a proficiency score based on problem-solving performance
        """
        if problems_attempted == 0:
            return 0.0
        return problems_correct / problems_attempted
