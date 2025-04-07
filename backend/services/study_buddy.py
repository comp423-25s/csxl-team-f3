"""
Service layer for the Rameses Study Buddy feature.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
import json
from backend.config import Config
from backend.models.academics.study_buddy import (
    StudyQuestion,
    DifficultyLevel,
    QuestionType,
    TopicProficiency,
    StudyPlan,
    ChatResponse
)

class StudyBuddyService:
    """Service class for handling study buddy operations."""
    
    def __init__(self):
        """Initialize the service with OpenAI configuration."""
        Config.validate_config()
        # self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.client = None
    
    async def _generate_with_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Helper method to generate content with OpenAI."""
        return json.dumps([
        {
            "question": "What is polymorphism?",
            "topic": "Object-Oriented Programming",
            "difficulty": "easy",
            "question_type": "short_answer",
            "options": None,
            "correct_answer": "Polymorphism allows objects to be treated as instances of their parent class.",
            "explanation": "It is the ability of different objects to respond to the same method call in different ways."
        }
    ])
    
    async def get_course_questions(
        self, 
        course_id: str,
        topic: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        question_type: Optional[QuestionType] = None,
        count: int = 3
    ) -> List[StudyQuestion]:
        """
        Get study questions for a specific course with optional filters.
        """
        system_prompt = """You are a helpful study assistant for computer science courses. 
        Generate high-quality study questions in JSON format. Each question should include:
        - question text
        - topic
        - difficulty level (easy, medium, hard)
        - question type (multiple_choice, short_answer, code, conceptual)
        - options (for multiple choice)
        - correct answer
        - explanation
        
        Format the response as a JSON array of questions."""
        
        user_prompt = f"""Generate {count} study questions for course {course_id}"""
        if topic:
            user_prompt += f" about {topic}"
        if difficulty:
            user_prompt += f" at {difficulty} difficulty"
        if question_type:
            user_prompt += f" of type {question_type}"
        
        try:
            response = await self._generate_with_openai(system_prompt, user_prompt)
            questions_data = json.loads(response)
            
            questions = []
            for i, q_data in enumerate(questions_data):
                questions.append(StudyQuestion(
                    id=str(i + 1),
                    question=q_data["question"],
                    course_id=course_id,
                    topic=q_data["topic"],
                    difficulty=q_data["difficulty"],
                    question_type=q_data["question_type"],
                    options=q_data.get("options"),
                    correct_answer=q_data.get("correct_answer"),
                    explanation=q_data.get("explanation")
                ))
            
            return questions
        except json.JSONDecodeError:
            raise Exception("Failed to parse OpenAI response as JSON")
        except Exception as e:
            raise Exception(f"Failed to generate questions: {str(e)}")
    
    async def get_study_plan(self, course_id: str) -> StudyPlan:
        """
        Generate a study plan for a student in a specific course.
        """
        system_prompt = """You are a helpful study assistant. Create a detailed study plan in JSON format.
        The plan should include:
        - list of topics
        - proficiency level for each topic (beginner, intermediate, advanced)
        - recommended study order
        - estimated study time in minutes
        
        Format the response as a JSON object."""
        
        user_prompt = f"""Create a comprehensive study plan for course {course_id} 
        focusing on computer science topics. Include all major concepts and their 
        relationships."""
        
        try:
            response = await self._generate_with_openai(system_prompt, user_prompt)
            plan_data = json.loads(response)
            
            return StudyPlan(
                course_id=course_id,
                topics=plan_data["topics"],
                proficiency_levels={
                    topic: TopicProficiency(level)
                    for topic, level in plan_data["proficiency_levels"].items()
                },
                recommended_study_order=plan_data["recommended_study_order"],
                estimated_study_time=plan_data["estimated_study_time"]
            )
        except json.JSONDecodeError:
            raise Exception("Failed to parse OpenAI response as JSON")
        except Exception as e:
            raise Exception(f"Failed to generate study plan: {str(e)}")
    
    async def ask_question(self, course_id: str, question: str) -> ChatResponse:
        """
        Process a question and generate a response using OpenAI.
        """
        system_prompt = """You are a helpful study assistant for computer science courses. 
        Provide clear, accurate, and educational responses. Include:
        - A detailed answer
        - Related topics
        - Confidence score (0.0 to 1.0)
        - Suggested follow-up questions
        
        Format the response as a JSON object."""
        
        user_prompt = f"""Course: {course_id}
        Question: {question}
        
        Please provide a comprehensive answer that helps the student understand the concept."""
        
        try:
            response = await self._generate_with_openai(system_prompt, user_prompt)
            response_data = json.loads(response)
            
            return ChatResponse(
                answer=response_data["answer"],
                related_topics=response_data["related_topics"],
                confidence_score=response_data["confidence_score"],
                suggested_follow_up_questions=response_data.get("suggested_follow_up_questions")
            )
        except json.JSONDecodeError:
            raise Exception("Failed to parse OpenAI response as JSON")
        except Exception as e:
            raise Exception(f"Failed to generate answer: {str(e)}") 