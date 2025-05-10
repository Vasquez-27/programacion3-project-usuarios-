from pydantic import BaseModel

class Parameter(BaseModel):
    code: int
    description: str