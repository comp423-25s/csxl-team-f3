from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, Enum):
    SHORT_ANSWER = "short_answer"
    MULTIPLE_CHOICE = "multiple_choice"
