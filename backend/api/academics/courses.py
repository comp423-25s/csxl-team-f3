"""Courses API

This API is used to access all courses data."""

from fastapi import APIRouter, Depends
from ...services.academics import CourseService
from ...models.academics import Course

__authors__ = ["AI"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/academics/courses")
openapi_tags = {
    "name": "Academics",
    "description": "Academic and course information are managed via these endpoints.",
}


@api.get("", tags=["Academics"])
def get_all_courses(course_service: CourseService = Depends()) -> list[Course]:
    """
    Get all courses

    Returns:
        list[Course]: All `Course`s in the `Course` database table
    """
    return course_service.all() 