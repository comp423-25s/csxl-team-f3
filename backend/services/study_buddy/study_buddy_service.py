from typing import List, Optional
from uuid import UUID
import openai
import os
from ...models import PracticeProblem, StudyGuide, StudentProgress


class StudyBuddyService:
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        # self.client = openai.OpenAI(api_key=api_key)
        self.client = None

    async def generate_study_guide(
        self,
        course_id: UUID,
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
        Create a comprehensive study guide for the following computer science topics:
        {', '.join(topics)}
        
        Focus especially on these areas where the student needs improvement:
        {', '.join(weak_topics)}
        
        The study guide should:
        1. Explain key concepts clearly and concisely
        2. Include relevant examples
        3. Provide step-by-step explanations for complex topics
        4. Include common pitfalls and how to avoid them
        5. Suggest additional resources for further study
        
        Format the study guide in markdown with clear sections and subsections.
        """

        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert computer science tutor.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return StudyGuide(
            course_id=course_id,
            topic=", ".join(topics),
            content=response.choices[0].message.content,
        )

    async def generate_practice_problem(
        self, course_id: UUID, topic: str, difficulty: str, question_type: str
    ) -> PracticeProblem:
        """
        Generate a practice problem using OpenAI
        """
        prompt = f"""
        Create a {difficulty} difficulty {question_type} question about {topic} in computer science.
        
        The question should:
        1. Test understanding of key concepts
        2. Be clear and unambiguous
        3. Include a detailed explanation of the correct answer
        4. Be appropriate for a computer science student
        
        Format the response as JSON with the following structure:
        {{
            "question_text": "The question text",
            "answer": "The correct answer",
            "explanation": "Detailed explanation of why this is the correct answer"
        }}
        """

        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert computer science educator.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )

        result = response.choices[0].message.content
        return PracticeProblem(
            course_id=course_id,
            topic=topic,
            difficulty=difficulty,
            question_type=question_type,
            **result,
        )

    def calculate_proficiency_score(
        self, problems_attempted: int, problems_correct: int
    ) -> float:
        """
        Calculate a proficiency score based on problem-solving performance
        """
        if problems_attempted == 0:
            return 0.0
        return problems_correct / problems_attempted
