from pydantic import BaseModel
from typing import Optional, Literal

# More table types can be added later if needed


class Course(BaseModel):
    course_id: int
    department_id: Optional[int]
    course_identifier: Optional[str]
    course_prefix: Optional[str]
    course_title: Optional[str]
    course_description: Optional[str]
    credits: Optional[float]
    course_level: Optional[str]
    is_repeatable: Optional[bool]


class Prerequisite(BaseModel):
    prerequisite_id: int
    prerequisite_group_id: Optional[int]
    prerequisite_course_id: Optional[int]
    negative_prerequisite: Optional[bool]
    min_grade: Optional[str]
    concurrent_allowed: Optional[bool]


class PrerequisiteGroup(BaseModel):
    prerequisite_group_id: int
    course_id: Optional[int]
    group_operator: Literal['AND', 'OR']
    parent_group_id: Optional[int]


class Department(BaseModel):
    department_id: int
    school_id: Optional[int]
    department_name: Optional[str]
