# Plan de Sesiones de Aprendizaje - Habit RPG

## 📚 Enfoque Pedagógico

Este plan está diseñado para aprender programación mientras construimos el proyecto. Cada sesión:
- **Explica conceptos** antes de implementarlos
- **Construye sobre conocimientos previos**
- **Incluye ejercicios prácticos**
- **Progresión de simple a complejo**

---

## 🎯 Sesión 0: Preparación y Conceptos Fundamentales

### Objetivos de Aprendizaje
- Entender qué es una aplicación fullstack
- Comprender la separación frontend/backend
- Familiarizarse con las herramientas básicas

### Conceptos a Explicar

#### ¿Qué es Fullstack?
**Analogía**: Imagina un restaurante:
- **Backend (Cocina)**: Donde se prepara la comida (lógica, base de datos)
- **Frontend (Sala)**: Donde los clientes ven y piden (interfaz web)
- **API (Camarero)**: Lleva pedidos de la sala a la cocina y trae la comida

#### ¿Qué es una API REST?
**Explicación simple**: 
- Es como un menú de restaurante con opciones numeradas
- El frontend "pide" datos usando URLs específicas
- El backend "sirve" los datos solicitados
- Ejemplo: `GET /api/users/me` = "Dame mi información de usuario"

#### ¿Qué es una Base de Datos?
**Explicación simple**:
- Como un Excel gigante pero más potente
- Guarda información de forma organizada en "tablas"
- Cada tabla tiene "columnas" (campos) y "filas" (registros)
- Ejemplo: Tabla "Users" con columnas: id, email, username

### Actividades
1. Instalar herramientas necesarias (Python, Node.js/Bun, Git)
2. Crear cuenta en Supabase (base de datos)
3. Crear cuenta en Clerk (autenticación)
4. Entender la estructura del proyecto

### Tiempo estimado: 1-2 horas

---

## 🐍 Sesión 1: Backend - Introducción a Python y FastAPI

### Objetivos de Aprendizaje
- Entender qué es Python y por qué lo usamos
- Aprender conceptos básicos de Python (variables, funciones, clases)
- Crear tu primer servidor web con FastAPI

### Conceptos a Explicar

#### Python Básico (Repaso)
```python
# Variables: Guardan información
nombre = "Fran"
edad = 25

# Funciones: Bloques de código reutilizables
def saludar(nombre):
    return f"Hola {nombre}"

# Clases: Plantillas para crear objetos
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
```

#### ¿Qué es FastAPI?
- Framework = Herramientas pre-construidas para hacer cosas comunes
- FastAPI = Framework para crear APIs rápidamente
- Similar a Express.js pero para Python

#### Tu Primer Endpoint
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola mundo!"}
```

**Explicación**:
- `@app.get("/")` = "Cuando alguien visite la raíz, haz esto"
- `def leer_raiz()` = Función que se ejecuta
- `return` = Lo que enviamos de vuelta

### Actividades Prácticas
1. Crear estructura de carpetas del backend
2. Instalar FastAPI y dependencias
3. Crear `main.py` con un endpoint simple
4. Probar el servidor localmente
5. Entender qué es `requirements.txt`

### Ejercicio
Crear 3 endpoints simples:
- `/` → Devuelve "Hola mundo"
- `/saludo/{nombre}` → Devuelve "Hola {nombre}"
- `/suma/{a}/{b}` → Devuelve la suma de a + b

### Tiempo estimado: 2-3 horas

---

## 🗄️ Sesión 2: Backend - Base de Datos con SQLAlchemy

### Objetivos de Aprendizaje
- Entender qué es un ORM (Object-Relational Mapping)
- Aprender a definir modelos de datos
- Conectar con Supabase (PostgreSQL)

### Conceptos a Explicar

#### ¿Qué es un ORM?
**Analogía**: 
- Sin ORM: Escribir SQL manualmente (como escribir en otro idioma)
- Con ORM: Usar Python para interactuar con la base de datos (tu idioma nativo)

**SQLAlchemy** = ORM para Python

#### ¿Qué es un Modelo?
**Explicación**:
- Un modelo es como un "molde" o "plantilla"
- Define cómo se ve una tabla en la base de datos
- Ejemplo: Modelo "User" define que hay columnas: id, email, username

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
```

**Explicación línea por línea**:
- `class User` = Definimos una clase llamada User
- `__tablename__` = Nombre de la tabla en la BD
- `id = Column(Integer, primary_key=True)` = Columna de tipo número, es la clave primaria (única)

#### Relaciones entre Tablas
**Analogía**: 
- User tiene muchos UserHabits (1 a muchos)
- Como una persona tiene muchos libros

```python
# En User
user_habits = relationship("UserHabit", back_populates="user")

# En UserHabit
user_id = Column(Integer, ForeignKey("users.id"))
user = relationship("User", back_populates="user_habits")
```

### Actividades Prácticas
1. Configurar conexión a Supabase
2. Crear archivo `database.py` con la conexión
3. Crear modelo `User` básico
4. Crear primera migración con Alembic
5. Aplicar migración a la base de datos

### Ejercicio
Crear modelo `Category` con campos: id, name, description

### Tiempo estimado: 2-3 horas

---

## 🔐 Sesión 3: Backend - Autenticación con Clerk

### Objetivos de Aprendizaje
- Entender qué es Clerk y por qué lo usamos
- Aprender a integrar servicios externos (BaaS - Backend as a Service)
- Verificar tokens de Clerk en el backend
- Sincronizar usuarios de Clerk con nuestra base de datos

### Conceptos a Explicar

#### ¿Qué es Clerk?
**Explicación**:
- Servicio de autenticación como servicio (Authentication as a Service)
- Maneja todo el proceso de autenticación por ti
- Registro, login, verificación de email, reset de password, OAuth (Google, GitHub, etc.)
- Muy usado en la industria moderna

**Ventajas**:
- No necesitas escribir código de autenticación
- Más seguro (ellos manejan la seguridad)
- UI pre-construida para frontend
- Ahorra mucho tiempo

#### ¿Cómo funciona Clerk?
**Flujo**:
1. Usuario se registra/loguea en el frontend (usando componentes de Clerk)
2. Clerk genera un token JWT
3. Frontend envía el token en cada petición al backend
4. Backend verifica el token con Clerk
5. Si es válido, permite el acceso

#### ¿Qué es un Webhook?
**Explicación simple**:
- Como un "callback" o "notificación"
- Cuando algo pasa en Clerk (ej: usuario se registra), Clerk te avisa
- Tu backend puede crear el usuario en tu BD automáticamente

**Ejemplo**:
- Usuario se registra en Clerk
- Clerk envía webhook a tu backend: "Usuario X se registró"
- Tu backend crea el usuario en tu BD

#### Verificación de Tokens
**En el backend**:
```python
from clerk_backend_sdk import Clerk

clerk = Clerk(api_key="tu_clave")

# Verificar token
user = clerk.verify_token(token)
clerk_user_id = user["id"]
```

### Actividades Prácticas
1. Crear cuenta en Clerk
2. Obtener API keys (clave pública y secreta)
3. Instalar `clerk-sdk-python` en el backend
4. Crear función para verificar tokens de Clerk
5. Crear middleware/dependency para proteger endpoints
6. Actualizar modelo User (añadir `clerk_user_id`)
7. Crear webhook handler para sincronizar usuarios
8. Probar autenticación con Postman/Thunder Client

### Ejercicio
Crear endpoint `/api/users/me` que:
- Verifica token de Clerk
- Obtiene `clerk_user_id` del token
- Busca usuario en BD por `clerk_user_id`
- Devuelve información del usuario

### Notas Importantes
- **No guardamos contraseñas**: Clerk las maneja
- **No creamos endpoints de registro/login**: Clerk los maneja
- **Solo verificamos tokens**: Para saber quién está autenticado
- **Sincronizamos usuarios**: Cuando Clerk crea un usuario, lo creamos en nuestra BD

### Tiempo estimado: 2-3 horas (más rápido que implementar JWT manualmente)

---

## 📝 Sesión 4: Backend - Pydantic y Validación de Datos

### Objetivos de Aprendizaje
- Entender qué es validación de datos
- Aprender a usar Pydantic
- Crear schemas (modelos de datos para API)

### Conceptos a Explicar

#### ¿Por qué validar datos?
**Analogía**: 
- Como revisar que un formulario esté bien lleno antes de procesarlo
- Evita errores y problemas de seguridad
- Asegura que los datos tienen el formato correcto

#### ¿Qué es Pydantic?
- Biblioteca para validar datos en Python
- Define "schemas" (plantillas) de cómo deben ser los datos
- Rechaza datos que no cumplan las reglas

**Ejemplo**:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str  # Debe ser texto
    password: str  # Debe ser texto
    username: str  # Debe ser texto
```

Si alguien envía `{"email": 123}`, Pydantic rechaza porque email debe ser texto.

#### Schemas vs Models
- **Model (SQLAlchemy)**: Define la tabla en la base de datos
- **Schema (Pydantic)**: Define qué datos acepta la API

**Diferencia**:
- Model = Cómo se guarda en BD
- Schema = Cómo se recibe/envía por API

### Actividades Prácticas
1. Crear schemas para User (Create, Response)
2. Crear schemas para Habit
3. Usar schemas en endpoints de registro
4. Validar datos de entrada
5. Formatear datos de salida

### Ejercicio
Crear schema `HabitCreate` con validación:
- name: texto, mínimo 3 caracteres
- description: texto opcional
- category_id: número entero

### Tiempo estimado: 2 horas

---

## 🛣️ Sesión 5: Backend - Crear Endpoints CRUD

### Objetivos de Aprendizaje
- Entender qué es CRUD (Create, Read, Update, Delete)
- Aprender a crear endpoints RESTful
- Implementar operaciones básicas de base de datos

### Conceptos a Explicar

#### ¿Qué es CRUD?
**Acrónimo**:
- **C**reate (Crear) → POST
- **R**ead (Leer) → GET
- **U**pdate (Actualizar) → PATCH/PUT
- **D**elete (Eliminar) → DELETE

**Ejemplo con User**:
- POST `/api/users` → Crear usuario
- GET `/api/users/me` → Leer mi usuario
- PATCH `/api/users/me` → Actualizar mi usuario
- DELETE `/api/users/me` → Eliminar mi usuario

#### Operaciones con SQLAlchemy
```python
# CREATE (Crear)
nuevo_usuario = User(email="test@test.com", username="test")
db.add(nuevo_usuario)
db.commit()

# READ (Leer)
usuario = db.query(User).filter(User.id == 1).first()

# UPDATE (Actualizar)
usuario.username = "nuevo_nombre"
db.commit()

# DELETE (Eliminar)
db.delete(usuario)
db.commit()
```

### Actividades Prácticas
1. Crear endpoints para Categories (GET all, GET one)
2. Crear endpoints para Habits (GET all, GET one, filtrar por categoría)
3. Crear endpoints para UserHabits (GET, POST, PATCH, DELETE)
4. Implementar autenticación en endpoints protegidos
5. Manejar errores (404, 400, 500)

### Ejercicio
Crear endpoint completo para Categories:
- GET `/api/categories` → Lista todas
- GET `/api/categories/{id}` → Obtiene una por ID
- Manejar error si no existe (404)

### Tiempo estimado: 3-4 horas

---

## 🧮 Sesión 6: Backend - Lógica de Negocio (XP, Niveles, Rachas)

### Objetivos de Aprendizaje
- Entender cómo calcular XP y niveles
- Implementar sistema de rachas
- Crear servicios reutilizables

### Conceptos a Explicar

#### ¿Qué es un Servicio?
**Explicación**:
- Funciones que contienen lógica de negocio
- Separadas de los endpoints (rutas)
- Reutilizables en diferentes partes del código

**Ejemplo**:
```python
# En services/xp_service.py
def calcular_nivel(xp: int) -> int:
    return int(sqrt(xp / 100)) + 1

# En routes/user_habits.py
nivel = calcular_nivel(usuario.global_xp)
```

#### Sistema de XP
**Fórmula**: `nivel = sqrt(xp / 100) + 1`

**Por qué esta fórmula?**
- Niveles más altos requieren más XP
- Crecimiento exponencial (cada vez más difícil)
- Ejemplo: Nivel 1 = 0 XP, Nivel 2 = 100 XP, Nivel 3 = 400 XP

#### Sistema de Rachas
**Lógica**:
1. Al completar hábito, verificar última fecha de completado
2. Si fue ayer → Incrementar racha
3. Si no fue ayer → Resetear racha a 1
4. Bonus XP = racha * 5 (máximo 50)

### Actividades Prácticas
1. Crear `services/xp_service.py` con función calcular_nivel
2. Crear `services/streak_service.py` con lógica de rachas
3. Crear `services/attribute_service.py` para actualizar atributos
4. Implementar endpoint `/api/user-habits/{id}/complete`
5. Calcular y guardar XP, coins, racha al completar

### Ejercicio
Crear función que:
- Recibe user_habit_id
- Calcula si hay racha (completado ayer)
- Actualiza current_streak y longest_streak
- Retorna el bonus de racha

### Tiempo estimado: 3-4 horas

---

## ⚛️ Sesión 7: Frontend - Introducción a React y TypeScript

### Objetivos de Aprendizaje
- Entender qué es React y por qué lo usamos
- Aprender conceptos básicos de React (componentes, props, estado)
- Introducción a TypeScript

### Conceptos a Explicar

#### ¿Qué es React?
**Analogía**: 
- Como bloques de LEGO
- Cada componente es un bloque reutilizable
- Puedes combinar bloques para hacer cosas complejas

**Componente simple**:
```tsx
function Saludo({ nombre }: { nombre: string }) {
  return <h1>Hola {nombre}</h1>;
}
```

**Explicación**:
- `function Saludo` = Definimos un componente
- `{ nombre }` = Recibe "props" (propiedades)
- `: { nombre: string }` = TypeScript: nombre debe ser texto
- `return <h1>...</h1>` = Devuelve HTML (JSX)

#### ¿Qué es el Estado?
**Explicación**:
- Datos que pueden cambiar
- Cuando cambian, React actualiza la pantalla automáticamente
- Se usa `useState`

**Ejemplo**:
```tsx
const [contador, setContador] = useState(0);

// contador = valor actual (0)
// setContador = función para cambiar el valor
```

#### ¿Qué es TypeScript?
**Explicación simple**:
- JavaScript con tipos
- Te ayuda a encontrar errores antes de ejecutar
- Como tener un corrector ortográfico para código

### Actividades Prácticas
1. Crear proyecto React con Vite
2. Instalar TypeScript
3. Crear componente simple "HolaMundo"
4. Crear componente con props
5. Crear componente con estado (contador)
6. Entender JSX básico

### Ejercicio
Crear componente `Contador` que:
- Muestra un número
- Tiene botón "+" para incrementar
- Tiene botón "-" para decrementar

### Tiempo estimado: 2-3 horas

---

## 🎨 Sesión 8: Frontend - Shadcn/ui y Tailwind CSS

### Objetivos de Aprendizaje
- Entender qué es un sistema de componentes
- Aprender a usar Tailwind CSS
- Instalar y usar Shadcn/ui

### Conceptos a Explicar

#### ¿Qué es Shadcn/ui?
**Explicación**:
- Biblioteca de componentes pre-construidos
- Botones, inputs, cards, etc.
- Personalizables y accesibles
- No es una dependencia, copias el código (más control)

#### ¿Qué es Tailwind CSS?
**Explicación**:
- Framework de CSS con clases utilitarias
- En lugar de escribir CSS, usas clases
- Ejemplo: `className="bg-blue-500 text-white p-4"`

**Comparación**:
```css
/* CSS tradicional */
.mi-boton {
  background-color: blue;
  color: white;
  padding: 1rem;
}
```

```tsx
/* Tailwind */
<button className="bg-blue-500 text-white p-4">
```

### Actividades Prácticas
1. Instalar Tailwind CSS
2. Configurar Tailwind
3. Instalar Shadcn/ui
4. Crear componentes básicos (Button, Input, Card)
5. Crear página de ejemplo con componentes

### Ejercicio
Crear componente de tarjeta (Card) usando Shadcn que:
- Tiene título
- Tiene descripción
- Tiene botón de acción
- Usa Tailwind para estilizar

### Tiempo estimado: 2 horas

---

## 🔌 Sesión 9: Frontend - Integrar Clerk y Conectar con Backend

### Objetivos de Aprendizaje
- Integrar Clerk en el frontend
- Entender cómo hacer peticiones HTTP con Axios
- Aprender a usar React Query para manejar estado del servidor
- Configurar interceptores para añadir tokens de Clerk

### Conceptos a Explicar

#### Integrar Clerk en React
**Explicación**:
- Clerk proporciona componentes y hooks listos para usar
- `<ClerkProvider>` envuelve tu app
- `<SignIn />` y `<SignUp />` son componentes pre-construidos
- `useUser()` hook para obtener usuario actual

**Ejemplo**:
```tsx
import { ClerkProvider, SignIn, SignUp } from '@clerk/clerk-react';

function App() {
  return (
    <ClerkProvider publishableKey="tu_clave_publica">
      <SignIn />
      <SignUp />
    </ClerkProvider>
  );
}
```

#### ¿Qué es Axios?
**Explicación**:
- Biblioteca para hacer peticiones HTTP
- Más fácil que fetch nativo
- Maneja errores mejor

**Ejemplo**:
```tsx
import axios from 'axios';

const respuesta = await axios.get('http://localhost:8000/api/users/me');
const datos = respuesta.data;
```

#### Interceptores de Axios
**Concepto**:
- Interceptan peticiones antes de enviarlas
- Perfecto para añadir el token de Clerk automáticamente
- No necesitas añadir el token manualmente en cada petición

**Ejemplo**:
```tsx
axios.interceptors.request.use((config) => {
  const token = getToken(); // Token de Clerk
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

#### ¿Qué es React Query?
**Explicación**:
- Maneja el estado de datos del servidor
- Cache automático (no pide datos que ya tienes)
- Actualización automática
- Manejo de loading y errores

**Ejemplo**:
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['users', 'me'],
  queryFn: () => api.getUser()
});
```

**Explicación**:
- `data` = Los datos del servidor
- `isLoading` = true mientras carga
- `error` = Si hay error

### Actividades Prácticas
1. Instalar `@clerk/clerk-react`
2. Configurar ClerkProvider en App.tsx
3. Configurar Axios con base URL
4. Configurar interceptores para añadir token de Clerk automáticamente
5. Crear servicio `api.ts` con funciones para llamar al backend
6. Crear hook `useUser` con React Query para obtener datos del usuario
7. Probar conexión con backend

### Ejercicio
Configurar Clerk y Axios para que:
- Clerk maneje registro/login automáticamente
- Cada petición al backend incluya el token de Clerk
- Podamos obtener datos del usuario desde el backend

### Notas Importantes
- **No creamos páginas de Login/Register**: Clerk las proporciona
- **Token se obtiene automáticamente**: Clerk lo maneja
- **Solo configuramos**: Integración, no implementación

### Tiempo estimado: 2-3 horas (más rápido que implementar auth manualmente)

---

## 📱 Sesión 10: Frontend - Crear Páginas Principales

### Objetivos de Aprendizaje
- Aprender React Router para navegación
- Crear páginas Dashboard y Habits
- Implementar protección de rutas

### Conceptos a Explicar

#### ¿Qué es React Router?
**Explicación**:
- Maneja la navegación entre páginas
- Cambia la URL sin recargar la página
- Como tener múltiples páginas en una sola aplicación

**Ejemplo**:
```tsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/login" element={<Login />} />
  <Route path="/dashboard" element={<Dashboard />} />
</Routes>
```

#### Protección de Rutas con Clerk
**Concepto**:
- Algunas páginas solo para usuarios logueados
- Si no estás logueado → Clerk redirige automáticamente a login

**Implementación con Clerk**:
```tsx
import { useAuth } from '@clerk/clerk-react';

function ProtectedRoute({ children }) {
  const { isSignedIn, isLoaded } = useAuth();
  
  if (!isLoaded) {
    return <div>Cargando...</div>;
  }
  
  if (!isSignedIn) {
    return <Navigate to="/sign-in" />;
  }
  
  return children;
}
```

**O usar componente de Clerk**:
```tsx
import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/clerk-react';

function ProtectedRoute({ children }) {
  return (
    <>
      <SignedIn>{children}</SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
}
```

### Actividades Prácticas
1. Configurar React Router
2. Crear layout principal
3. Integrar Clerk con React Router
4. Crear página Dashboard (mostrar datos del usuario)
5. Crear página Habits (listar hábitos disponibles)
6. Implementar protección de rutas con Clerk
7. Crear navegación entre páginas

### Ejercicio
Crear Dashboard protegido que:
- Solo accesible si estás logueado (Clerk)
- Muestra nombre de usuario (desde Clerk)
- Muestra nivel global (desde backend)
- Muestra XP total (desde backend)
- Lista de hábitos activos (desde backend)

### Tiempo estimado: 3-4 horas

---

## 🎯 Sesión 11: Frontend - Implementar Features Core

### Objetivos de Aprendizaje
- Activar hábitos desde el frontend
- Completar hábitos
- Ajustar dificultad
- Ver progreso en tiempo real

### Conceptos a Explicar

#### Mutaciones con React Query
**Explicación**:
- `useQuery` = Para leer datos (GET)
- `useMutation` = Para modificar datos (POST, PATCH, DELETE)

**Ejemplo**:
```tsx
const mutation = useMutation({
  mutationFn: (habitId) => api.activateHabit(habitId),
  onSuccess: () => {
    queryClient.invalidateQueries(['user-habits']);
  }
});

// Usar
mutation.mutate(habitId);
```

#### Optimistic Updates
**Concepto**:
- Actualizar la UI antes de que el servidor responda
- Mejor experiencia de usuario (más rápido)
- Si falla, se revierte

### Actividades Prácticas
1. Crear hook `useHabits` con queries y mutations
2. Implementar activar hábito (con selección de nivel)
3. Implementar completar hábito
4. Implementar ajustar dificultad
5. Actualizar Dashboard en tiempo real
6. Mostrar rachas y progreso

### Ejercicio
Crear componente `HabitCard` que:
- Muestra información del hábito
- Botón "Activar" si no está activo
- Botón "Completar" si está activo
- Muestra racha actual
- Permite ajustar dificultad

### Tiempo estimado: 4-5 horas

---

## 🚀 Sesión 12: Deploy y Finalización

### Objetivos de Aprendizaje
- Entender qué es deploy
- Aprender a desplegar en Vercel (frontend) y Render (backend)
- Configurar variables de entorno

### Conceptos a Explicar

#### ¿Qué es Deploy?
**Explicación simple**:
- Subir tu aplicación a internet
- Hacerla accesible para otros
- Como publicar un sitio web

#### Variables de Entorno
**Concepto**:
- Datos sensibles (passwords, API keys) no deben estar en el código
- Se guardan en variables de entorno
- Diferentes valores para desarrollo y producción

**Ejemplo**:
```python
# .env (local, no se sube a Git)
DATABASE_URL=postgresql://...
SECRET_KEY=mi_clave_secreta

# En código
import os
database_url = os.getenv("DATABASE_URL")
```

### Actividades Prácticas
1. Preparar backend para producción
2. Configurar variables de entorno en Render
3. Deploy backend en Render
4. Preparar frontend para producción
5. Configurar variables de entorno en Vercel
6. Deploy frontend en Vercel
7. Probar aplicación en producción

### Ejercicio
Hacer deploy completo y verificar que:
- Backend responde correctamente
- Frontend se conecta al backend
- Autenticación funciona
- Todas las features funcionan

### Tiempo estimado: 2-3 horas

---

## 📊 Resumen del Plan

### Backend (Sesiones 1-6)
- **Sesión 1**: FastAPI básico
- **Sesión 2**: Base de datos y modelos
- **Sesión 3**: Autenticación
- **Sesión 4**: Validación con Pydantic
- **Sesión 5**: Endpoints CRUD
- **Sesión 6**: Lógica de negocio

### Frontend (Sesiones 7-11)
- **Sesión 7**: React y TypeScript
- **Sesión 8**: Shadcn/ui y Tailwind
- **Sesión 9**: Conectar con backend
- **Sesión 10**: Páginas principales
- **Sesión 11**: Features core

### Deploy (Sesión 12)
- Deploy en producción

### Tiempo Total Estimado: 30-40 horas

---

## 💡 Consejos de Aprendizaje

1. **No tengas prisa**: Mejor entender bien que avanzar rápido
2. **Experimenta**: Cambia valores, prueba cosas, rompe el código
3. **Pregunta**: Si algo no entiendes, pregunta
4. **Practica**: Después de cada sesión, intenta hacer variaciones
5. **Documenta**: Escribe notas de lo que aprendes

---

## 🎓 Recursos Adicionales

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

---

¡Vamos a construir algo increíble! 🚀
