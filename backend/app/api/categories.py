from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """
    Lista todas las categorías.
    
    response_model=List[CategoryResponse] hace que FastAPI:
    1. Serialice los resultados usando CategoryResponse
    2. Documente la respuesta en Swagger
    """
    return db.query(Category).all()
    


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una categoría por ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {category_id} no encontrada"
        )
    
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,  # FastAPI valida automáticamente
    db: Session = Depends(get_db)
):
    """
    Crea una nueva categoría.
    
    category_data: CategoryCreate - FastAPI:
    1. Parsea el JSON del request body
    2. Valida según el schema
    3. Si falla, devuelve error 422 automáticamente
    """
    # Verificar que no exista
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una categoría con el nombre '{category_data.name}'"
        )
    
    # Crear la categoría
    new_category = Category(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category