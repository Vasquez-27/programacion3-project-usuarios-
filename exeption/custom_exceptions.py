from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class InternalServerException(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)