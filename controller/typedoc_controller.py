from fastapi import APIRouter, HTTPException, status, Depends
from model.typedoc import Typedoc
from service.typedoc_service import TypedocService, get_typedoc_service
from typing import List

typedoc_router = APIRouter()

@typedoc_router.get("/typedocs", response_model=List[Typedoc])
def list_typedocs(service: TypedocService = Depends(get_typedoc_service)) -> List[Typedoc]:
    return service.get_all_typedocs()

@typedoc_router.post("/typedocs", response_model=Typedoc, status_code=status.HTTP_201_CREATED)
def create_typedoc(typedoc: Typedoc, service: TypedocService = Depends(get_typedoc_service)) -> Typedoc:
    return service.create_typedoc(typedoc)