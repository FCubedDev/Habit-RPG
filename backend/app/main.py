"""
Habit-RPG Backend - Punto de entrada principal

Este archivo es donde empieza toda la aplicación.
FastAPI lo utiliza para definir los endpoints de la API.
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models import Category
from app.api.webhooks import router as webhooks_router
from app.api.users import router as users_router
import math

# ============================================================
# CREAR LA APLICACIÓN
# ============================================================
# FastAPI() crea una instancia de la aplicación.
# Los parámetros son opcionales pero útiles para documentación.

app = FastAPI(
    title="Habit-RPG API",
    description="API para la aplicación de gamificación de hábitos",
    version="0.1.0"
)

# Registrar routers
app.include_router(webhooks_router)
app.include_router(users_router)

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def raiz():
    """
    Endpoint raíz - Saludo de bienvenida.
    
    Cuando alguien visita http://localhost:8000/
    verá este mensaje.
    """
    return {
        "mensaje": "¡Bienvenido a Habit-RPG API!",
        "version": "0.1.0",
        "documentacion": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check - Para verificar que el servidor funciona.
    
    Es una buena práctica tener un endpoint que devuelva
    'ok' para saber que el servidor está vivo.
    """
    return {"status": "ok"}

@app.get("/suma/{a}/{b}")
def sumar(a: int, b: int):
    """
    Suma dos números.
    
    Los parámetros se convierten automáticamente a int.
    Si envías texto, FastAPI devuelve un error.
    """
    resultado = a + b
    return {
        "operacion": f"{a} + {b}",
        "resultado": resultado
    }

@app.get("/calcular-xp")
def calcular_xp(base: int, multiplicador: float = 1.0, bonus_racha: int = 0):
    """
    Calcula el XP ganado.
    
    - base: XP base del hábito (obligatorio)
    - multiplicador: Según dificultad (opcional, default=1.0)
    - bonus_racha: Bonus por racha (opcional, default=0)
    
    Ejemplo: GET /calcular-xp?base=100&multiplicador=1.5&bonus_racha=10
    """
    xp_total = int(base * multiplicador) + bonus_racha
    return {
        "base": base,
        "multiplicador": multiplicador,
        "bonus_racha": bonus_racha,
        "xp_total": xp_total
    }

@app.get("/nivel/{xp}")
def calcular_nivel(xp: int):
    """
    Calcula el nivel basado en el XP total.
    
    Usa la fórmula: `nivel = sqrt(xp / 100) + 1`
    
    - **xp**: Puntos de experiencia totales
    """
    nivel = int(math.sqrt(xp / 100)) + 1
    return {
        "xp": xp,
        "nivel": nivel
    }
@app.get("/divide/{a}/{b}")
def divide(a : float, b : float):
    if b == 0:
    # Esto devuelve un error 400 Bad Request
        raise HTTPException(status_code=400, detail="No se puede dividir entre 0")
    else:
        return {"result": a/b}

@app.get("/factorial/{a}")
def factorial(a : int):
    result=1
    for i in range(a,0,-1):
        result = result * i
    return {
        "operation":f"{a}!",
        "result":result
    }

@app.get("/bonus-racha")
def bonusRacha(diasConsecutivos:int):
    result = min(50,diasConsecutivos*5)
    return {
        "dias": diasConsecutivos,
        "bonus": result,
        "maximoAlcanzado": True if diasConsecutivos*5>=50 else False
    }

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    """
    Prueba la conexión a la base de datos.
    
    Ejecuta una consulta simple para verificar que todo funciona.
    """
    try:
        # Ejecutar consulta simple
        result = db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "mensaje": "Conexión a base de datos exitosa"
        }
    except Exception as e:
        return {
            "status": "error",
            "mensaje": str(e)
        }
    
@app.get("/categories")
def show_categories(db : Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [
        {
            "id" : cat.id,
            "name" : cat.name,
            "description" : cat.description,
            "icon" : cat.icon
        }
        for cat in categories
    ]