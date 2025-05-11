from fastapi import APIRouter, HTTPException, status, Depends
from model.location import Location
from service.location_service import LocationService, get_location_service
from typing import List

location_router = APIRouter()

# ✅ Esta ruta funciona como /api/v1/locations
@location_router.get("/", response_model=List[Location])
def list_locations(service: LocationService = Depends(get_location_service)) -> List[Location]:
    return service.get_all_locations()

# ✅ Esta ruta funciona como /api/v1/locations/{location_code}
@location_router.get("/{location_code}", response_model=Location)
def get_location(location_code: int, service: LocationService = Depends(get_location_service)) -> Location:
    location = service.get_location_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found.")
    return location