from pydantic import BaseModel, Field
from typing import Optional

class Experience(BaseModel):
    """Model to represent a single experience found in the documents"""

    company: str = Field(description="The company name")
    title: str = Field(description="The title of the candidate")
    start_date: str = Field(description="The start date of the candidate's experience, in format MM/YYYY")
    end_date: Optional[str] = Field(description="The end date of the candidate's experience")
    description: str = Field(description="The description of the candidate's experience") 