from pydantic import BaseModel, Field
from typing import Optional

class RequirementAssessment(BaseModel):
    """Model to represent the assessment of a requirement against the candidate's documents"""
    requirement: str = Field(description="The requirement expressed in the job post")
    present_in_documents: bool = Field(description="Whether is it reasonable to expect the requirement is met based on the provided documents")
    inquiry: Optional[str] = Field(description="A clarifying question about to ask to the candidate when the requirement doesn't seem to be met in the documents") 