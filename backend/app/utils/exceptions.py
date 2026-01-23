"""
Excepciones personalizadas para la API.
"""
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Recurso no encontrado."""
    def __init__(self, resource: str, resource_id: int = None):
        detail = f"{resource} no encontrado"
        if resource_id:
            detail = f"{resource} con ID {resource_id} no encontrado"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class DuplicateException(HTTPException):
    """Recurso duplicado."""
    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un {resource} con {field} = '{value}'"
        )


class ForbiddenException(HTTPException):
    """Acción no permitida."""
    def __init__(self, message: str = "No tienes permiso para esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class BadRequestException(HTTPException):
    """Datos inválidos o petición incorrecta."""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )