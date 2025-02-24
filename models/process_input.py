from pydantic import BaseModel
from typing import List

class ProcessInput(BaseModel):
    job_requirements: List[str] 