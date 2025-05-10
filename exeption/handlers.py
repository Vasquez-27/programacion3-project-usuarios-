from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .custom_exceptions import NotFoundException, BadRequestException, InternalServerException

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(InternalServerException)
    async def internal_server_exception_handler(request: Request, exc: InternalServerException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        # Fallback for all other unhandled exceptions
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred"},
        )