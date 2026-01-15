# Habit Tracker MVP Simplificado

## Alcance del MVP

### Incluido

- **Usuario**: Registro, login, perfil con niveles, atributos, monedas (guardadas pero no usables aún)
- **Categorías**: Agrupaciones temáticas (Deporte, Lectura, Aprendizaje de software)
- **Misiones Diarias**: Hábitos que el usuario puede activar y completar
- **Sistema de Progresión**: XP, niveles globales y por categoría, atributos, rachas
- **Dificultad Adaptativa**: Usuario auto-evalúa nivel inicial y puede ajustar dificultad

### Excluido (para futuras versiones)

- Sistema de amigos
- Tienda/avatares (monedas existen pero no tienen uso aún)
- Logros/achievements
- Notificaciones

## Modelos de Datos Simplificados

### User

```python
- id: int (PK)
- email: str (unique)
- password_hash: str
- username: str
- global_level: int (nivel global calculado)
- global_xp: int (XP total acumulada)
- coins: int (moneda virtual - guardada pero no usada)
- created_at: datetime
- updated_at: datetime
```

### Category

```python
- id: int (PK)
- name: str (unique) # "Deporte", "Lectura", "Aprendizaje de software"
- description: str
- icon: str (nombre de icono)
- color: str (hex color)
- created_at: datetime
```

### Habit (Misiones)

```python
- id: int (PK)
- name: str
- description: str
- category_id: int (FK -> Category)
- target_type: str # "steps", "pages", "hours", "boolean"
- difficulty_levels: JSON # {
    "beginner": {"target": 2000, "xp_reward": 50},
    "intermediate": {"target": 5000, "xp_reward": 100},
    "advanced": {"target": 10000, "xp_reward": 200}
  }
- is_active: bool
- created_at: datetime
```

### UserHabit (Hábito activo del usuario)

```python
- id: int (PK)
- user_id: int (FK -> User)
- habit_id: int (FK -> Habit)
- self_assessed_level: str # "beginner", "intermediate", "advanced"
- current_difficulty: str # Puede ser diferente si el usuario la subió
- is_active: bool
- current_streak: int (días consecutivos)
- longest_streak: int (récord personal)
- total_completions: int
- created_at: datetime
- updated_at: datetime
```

### HabitCompletion (Registro de completos)

```python
- id: int (PK)
- user_habit_id: int (FK -> UserHabit)
- completed_at: datetime
- target_achieved: float/int (valor alcanzado)
- target_required: float/int (objetivo requerido)
- difficulty_level: str
- xp_earned: int
- coins_earned: int (guardado pero no usado aún)
- streak_bonus: int
- created_at: datetime
```

### UserAttribute (Atributos del usuario)

```python
- id: int (PK)
- user_id: int (FK -> User)
- attribute_name: str # "strength", "intelligence", "endurance", "creativity"
- points: int (puntos actuales)
- category_id: int (FK -> Category, nullable)
- created_at: datetime
- updated_at: datetime
```

## API Endpoints Simplificados

### Autenticación (`/api/auth`)

- `POST /api/auth/register` - Registro
- `POST /api/auth/login` - Login (JWT)
- `GET /api/auth/me` - Usuario actual

### Usuarios (`/api/users`)

- `GET /api/users/me` - Perfil completo
- `PATCH /api/users/me` - Actualizar perfil
- `GET /api/users/me/stats` - Estadísticas (XP, niveles, rachas)

### Categorías (`/api/categories`)

- `GET /api/categories` - Listar todas
- `GET /api/categories/{id}` - Detalle

### Hábitos (`/api/habits`)

- `GET /api/habits` - Listar todos (disponibles desde inicio)
- `GET /api/habits/{id}` - Detalle
- `GET /api/habits?category_id={id}` - Filtrar por categoría

### Hábitos del Usuario (`/api/user-habits`)

- `GET /api/user-habits` - Hábitos activos
- `POST /api/user-habits` - Activar hábito
  - Body: `{habit_id, self_assessed_level}`
- `PATCH /api/user-habits/{id}` - Actualizar (cambiar dificultad, desactivar)
- `DELETE /api/user-habits/{id}` - Desactivar
- `POST /api/user-habits/{id}/complete` - Completar hábito (validación manual)
  - Body: `{target_achieved}` (opcional)

### Completos (`/api/completions`)

- `GET /api/completions` - Historial del usuario
- `GET /api/completions?user_habit_id={id}` - Completos de un hábito

### Atributos (`/api/attributes`)

- `GET /api/attributes/me` - Atributos del usuario

## Lógica de Negocio

### Sistema de XP y Niveles

- **XP Global**: Suma de XP de todas las categorías
- **Nivel Global**: `level = int(sqrt(global_xp / 100)) + 1`
- **Nivel por Categoría**: Calculado desde XP ganada en esa categoría
- **XP por Completo**: Base según dificultad + bonus por racha

### Sistema de Rachas

- Al completar, verificar si se completó ayer
- Si sí: `current_streak += 1`
- Si no: `current_streak = 1`
- Actualizar `longest_streak` si es mayor
- Bonus: `streak_bonus = min(current_streak * 5, 50)` (máx 50 XP)

### Sistema de Atributos

- Cada categoría tiene atributos asociados
- Al completar hábito: incrementar atributos de esa categoría
- Ejemplo: Deporte → +1 Strength, +1 Endurance

### Sistema de Dificultad

1. Usuario activa hábito y selecciona nivel inicial (Principiante/Intermedio/Avanzado)
2. Se guarda en `self_assessed_level`
3. Usuario puede subir `current_difficulty` cuando quiera
4. Recompensas basadas en `current_difficulty`

### Cálculo de Recompensas

```python
base_xp = habit.difficulty_levels[current_difficulty]["xp_reward"]
streak_bonus = min(user_habit.current_streak * 5, 50)
total_xp = base_xp + streak_bonus
coins = total_xp // 10  # Guardado pero no usado
```

## Estructura de Carpetas Simplificada

```
habit-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py              # Configuración
│   │   ├── database.py            # SQLAlchemy setup
│   │   ├── models/                # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── category.py
│   │   │   ├── habit.py
│   │   │   ├── user_habit.py
│   │   │   ├── completion.py
│   │   │   └── attribute.py
│   │   ├── schemas/               # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── habit.py
│   │   │   └── completion.py
│   │   ├── api/                   # API routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py           # Dependencies (auth, db)
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── categories.py
│   │   │       ├── habits.py
│   │   │       ├── user_habits.py
│   │   │       ├── completions.py
│   │   │       └── attributes.py
│   │   ├── services/             # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── xp_service.py     # Cálculo XP y niveles
│   │   │   ├── streak_service.py # Lógica de rachas
│   │   │   └── attribute_service.py
│   │   └── utils/                # Utilidades
│   │       ├── __init__.py
│   │       └── security.py       # JWT, password hashing
│   ├── alembic/                  # Migraciones
│   ├── requirements.txt
│   ├── .env
│   └── .ruff.toml
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ui/               # Shadcn components
    │   │   ├── habits/
    │   │   └── dashboard/
    │   ├── pages/
    │   │   ├── Login.tsx
    │   │   ├── Register.tsx
    │   │   ├── Dashboard.tsx
    │   │   └── Habits.tsx
    │   ├── hooks/
    │   │   ├── useAuth.ts
    │   │   └── useHabits.ts
    │   ├── services/
    │   │   ├── api.ts            # Axios instance
    │   │   ├── auth.ts
    │   │   └── habits.ts
    │   ├── types/
    │   │   └── index.ts
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    ├── tsconfig.json
    └── vite.config.ts
```

## Flujo de Usuario Simplificado

1. **Registro/Login** → Obtiene JWT
2. **Dashboard** → Ve progreso, nivel, XP, atributos, hábitos activos, rachas
3. **Explorar Hábitos** → Ve todos los hábitos, filtra por categoría
4. **Activar Hábito** → Selecciona hábito, elige nivel inicial (Principiante/Intermedio/Avanzado)
5. **Completar Hábito** → Marca como completado manualmente, gana XP/coins
6. **Ajustar Dificultad** → Sube dificultad cuando se sienta listo
7. **Ver Progreso** → Dashboard actualizado con nuevos niveles y atributos

## Validación Manual

- Usuario hace click en "Completar" en el hábito
- Si tiene target numérico (ej: pasos), puede ingresar valor alcanzado
- Si es booleano (ej: "Meditar"), solo confirma completado
- Sistema calcula XP, coins, actualiza racha y atributos automáticamente
