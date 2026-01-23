from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )

"""
Su uso sería:
@router.get("/", response_model=PaginatedResponse[HabitResponse])
def list_habits_paginated(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total = db.query(Habit).count()
    habits = db.query(Habit).offset((page-1)*page_size).limit(page_size).all()
    return PaginatedResponse.create(habits, total, page, page_size)
"""