from pydantic import BaseModel, Field
from typing import List
from .experience import Experience

class CandidateData(BaseModel):
    """Model to represent the candidate data found in the documents"""
    first_name: str = Field(description="The first name of the candidate")
    last_name: str = Field(description="The last name of the candidate")
    email: str = Field(description="The email of the candidate")
    phone: str = Field(description="The phone number of the candidate")
    linkedin: str = Field(description="The LinkedIn profile of the candidate")
    experiences: List[Experience] = Field(description="The experiences of the candidate") 