from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Role(BaseModel):
    id: str
    name: str
    description: str
    permissions: List[str] = []
    priority: int = Field(default=5, ge=1, le=10)

