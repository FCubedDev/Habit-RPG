"""
Schemas de Pydantic para la API.

Los schemas definen la estructura de datos para:
- Entradas (Request bodies)
- Salidas (Responses)
- Validación automática
"""
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserStatsResponse,
    UserProfileResponse
)
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryWithHabitsResponse
)
from app.schemas.habit import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
    HabitWithCategoryResponse
)
from app.schemas.user_habit import (
    UserHabitCreate,
    UserHabitUpdate,
    UserHabitResponse,
    UserHabitDetailResponse,
    CompleteHabitResponse
)

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserStatsResponse",
    "UserProfileResponse",
    # Category
    "CategoryCreate",
    "CategoryResponse",
    "CategoryWithHabitsResponse",
    # Habit
    "HabitCreate",
    "HabitUpdate",
    "HabitResponse",
    "HabitWithCategoryResponse",
    # UserHabit
    "UserHabitCreate",
    "UserHabitUpdate",
    "UserHabitResponse",
    "UserHabitDetailResponse",
    "CompleteHabitResponse",
    #Pagination
    "PaginatedResponse",
]