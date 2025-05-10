from fastapi import FastAPI

# Routers
from controller.person_controller import person_router
from controller.typedoc_controller import typedoc_router
from controller.location_controller import location_router

# Servicios y setters
from service.location_service import LocationService, set_location_service
from service.person_service import PersonService, set_person_service
from service.typedoc_service import TypedocService, set_typedoc_service

# Manejo de excepciones
from exception.handlers import register_exception_handlers

# Crear la app
app = FastAPI(title="Person Management API", version="1.0.0")

# Inicializar servicios
location_service = LocationService(csv_path="CSV/DIVIPOLA.csv")
set_location_service(location_service)

person_service = PersonService(csv_path="data/persons.csv")
set_person_service(person_service)

typedoc_service = TypedocService(csv_path="CSV/DIVIPOLA.csv")
set_typedoc_service(typedoc_service)

# Incluir routers
app.include_router(person_router, prefix="/api/v1/persons", tags=["Persons"])
app.include_router(typedoc_router, prefix="/api/v1/typedocs", tags=["TypeDocs"])
app.include_router(location_router, prefix="/api/v1/locations", tags=["Locations"])

# Registrar excepciones personalizadas
register_exception_handlers(app)

# Ejecutar con Uvicorn si se corre directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)