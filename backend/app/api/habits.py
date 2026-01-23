from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Habit
from app.schemas import HabitResponse


router = APIRouter(prefix="/api/habits", tags=["Habits"])

@router.get("/", response_model=List[HabitResponse])
def list_habits(category_id : Optional[int] = None, db: Session = Depends(get_db)):
    if category_id:
        return db.query(Habit).filter(Habit.category_id == category_id).all()
    return db.query(Habit).all()


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hábito con ID {habit_id} no encontrado"
        )
    return habit