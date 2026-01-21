"""
Script para poblar la base de datos con datos iniciales.
"""
from app.database import SessionLocal
from app.models import Category, Habit

def seed_categories_and_habits():
    """Inserta categorías y hábitos de ejemplo."""
    db = SessionLocal()
    
    try:
        # Crear categorías
        categorias = [
            Category(name="Deporte", description="Actividades físicas", icon="🏃"),
            Category(name="Lectura", description="Hábitos de lectura", icon="📚"),
            Category(name="Productividad", description="Organización y trabajo", icon="💼"),
            Category(name="Salud", description="Bienestar físico y mental", icon="❤️"),
        ]
        
        for cat in categorias:
            db.add(cat)
        
        db.commit()
        print("✅ Categorías creadas")
        
        # Obtener IDs de categorías
        deporte = db.query(Category).filter(Category.name == "Deporte").first()
        lectura = db.query(Category).filter(Category.name == "Lectura").first()
        productividad = db.query(Category).filter(Category.name == "Productividad").first()
        salud = db.query(Category).filter(Category.name == "Salud").first()
        
        # Crear hábitos
        habitos = [
            Habit(name="Caminar 30 minutos", category_id=deporte.id, base_xp=50),
            Habit(name="Hacer 50 flexiones", category_id=deporte.id, base_xp=75),
            Habit(name="Leer 20 páginas", category_id=lectura.id, base_xp=40),
            Habit(name="Meditar 10 minutos", category_id=salud.id, base_xp=35),
            Habit(name="Completar una tarea pendiente", category_id=productividad.id, base_xp=60),
        ]
        
        for hab in habitos:
            db.add(hab)
        
        db.commit()
        print("✅ Hábitos creados")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_categories_and_habits()