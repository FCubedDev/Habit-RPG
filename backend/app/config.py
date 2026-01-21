"""
Configuración de la aplicación.

Lee las variables de entorno y las expone como configuración.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..","..",".env")

class Settings(BaseSettings):
    """
    Configuración basada en variables de entorno.
    
    Pydantic valida automáticamente que existan las variables requeridas.
    """
    # Base de datos
    database_url: str
    
    # Entorno
    environment: str = "development"
    
    model_config = SettingsConfigDict(
        # Archivo donde buscar las variables
        # Buscamos en el directorio actual (backend/.env)
        env_file = ENV_PATH,
        # No distinguir mayúsculas/minúsculas
        env_file_encoding = "utf-8",
        # Si hay un archivo extra para variables no definidas, lo ignora en vez de fallar
        extra = "ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la configuración (con cache).
    
    @lru_cache() evita leer el archivo .env cada vez.
    Solo lo lee una vez y luego reutiliza el resultado.
    """
    return Settings()


# Exponer configuración
settings = get_settings()
