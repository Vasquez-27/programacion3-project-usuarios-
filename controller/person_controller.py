from fastapi import APIRouter, HTTPException, status, Depends
from model.person import Person
from service.person_service import PersonService, get_person_service
from typing import List

person_router = APIRouter()

@person_router.post("/persons", response_model=Person, status_code=status.HTTP_201_CREATED)
def create_person(person: Person, service: PersonService = Depends(get_person_service)) -> Person:
    success = service.create_person(person)
    if not success:
        raise HTTPException(status_code=400, detail="Person could not be created.")
    return person

@person_router.get("/persons", response_model=List[Person])
def list_persons(service: PersonService = Depends(get_person_service)) -> List[Person]:
    return service.get_all_persons()

@person_router.get("/persons/{person_id}", response_model=Person)
def get_person(person_id: str, service: PersonService = Depends(get_person_service)) -> Person:
    person = service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found.")
    return person

@person_router.put("/persons/{person_id}", response_model=Person)
def update_person(person_id: str, updated_person: Person, service: PersonService = Depends(get_person_service)) -> Person:
    success = service.update_person(person_id, updated_person)
    if not success:
        raise HTTPException(status_code=404, detail="Person not found.")
    return updated_person

@person_router.delete("/persons/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: str, service: PersonService = Depends(get_person_service)) -> None:
    if not service.delete_person(person_id):
        raise HTTPException(status_code=404, detail="Person not found.")