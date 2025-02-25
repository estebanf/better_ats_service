from pydantic import BaseModel, Field
from typing import List, Optional
from .experience import Experience

class CandidateData(BaseModel):
    """Model to represent the candidate data found in the documents"""
    first_name: Optional[str] = Field(description="The first name of the candidate")
    last_name: Optional[str] = Field(description="The last name of the candidate")
    email: Optional[str] = Field(description="The email of the candidate")
    phone: Optional[str] = Field(description="The phone number of the candidate")
    linkedin: Optional[str] = Field(description="The LinkedIn profile of the candidate")
    experiences: List[Experience] = Field(description="The experiences of the candidate") 