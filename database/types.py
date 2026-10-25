from pydantic import BaseModel
from typing import Optional

# More table types can be added later if needed


class Course(BaseModel):
    course_id: int
    department_id: int
    course_identifier: str
    course_prefix: str
    course_title: str
    course_description: Optional[str]
    credits: float
    course_level: str
    is_repeatable: bool


class Prerequisite(BaseModel):
    prerequisite_id: int
    prerequisite_group_id: int
    prerequisite_course_id: int
    negative_prerequisite: bool
    min_grade: Optional[str]
    concurrent_allowed: bool


class PrerequisiteGroup(BaseModel):
    prerequisite_group_id: int
    course_id: int
    group_operator: str
    parent_group_id: Optional[int]


class Department(BaseModel):
    department_id: int
    school_id: int
    department_name: str
