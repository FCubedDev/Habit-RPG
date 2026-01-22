from app.database import SessionLocal
from app.models import User
db = SessionLocal()
clerk_id = "user_38aDfiithgDG5xVMmGn2AFCD14i" # <--- PEGA AQUÍ TU ID
# Crear el usuario manualmente
new_user = User(
    clerk_user_id=clerk_id,
    email="tu-email@ejemplo.com",
    username="Héroe de Prueba",
    global_xp=0,
    global_level=1,
    coins=100
)
db.add(new_user)
db.commit()
print(f"✅ Usuario {clerk_id} creado en la base de datos local.")