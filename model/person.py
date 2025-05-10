from pydantic import BaseModel
from .location import Location
from .typedoc import Typedoc

class Person(BaseModel):
    id: str
    name: str
    lastname: str
    age: int
    gender: str
    typedoc: Typedoc
    location: Location