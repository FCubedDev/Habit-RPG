"""
Modelos de la base de datos.

Importar desde aquí para tener acceso a todos los modelos.
"""
from app.models.user import User
from app.models.category import Category
from app.models.habit import Habit
from app.models.user_habit import UserHabit

# Esto permite hacer: from app.models import User, Category, Habit, UserHabit
__all__ = ["User", "Category", "Habit", "UserHabit"]