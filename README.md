# Sistema CRUD con Análisis de Mercado

Proyecto full-stack con Angular, FastAPI, SQLite y análisis de criptomonedas en tiempo real.

## Tecnologías

- **Frontend**: Angular 19
- **Backend**: FastAPI (Python)
- **Base de Datos**: SQLite
- **API Externa**: CoinGecko (precios de criptomonedas)

## Requisitos Previos

- Node.js 18+
- Python 3.8+
- Angular CLI: `npm install -g @angular/cli`

## Instalación

### 1. Backend (FastAPI)
```bash
cd backend
pip install fastapi uvicorn
```

### 2. Frontend (Angular)
```bash
cd frontend-angular
npm install
```

## Ejecución

Necesitas **2 terminales** abiertas simultáneamente:

### Terminal 1 - Backend
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

El backend estará en: http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend-angular
ng serve
```

El frontend estará en: http://localhost:4200

## Uso

1. **CRUD de Productos**: Crear, editar, listar y eliminar productos
2. **Precios en Tiempo Real**: Ver precios actuales de criptomonedas
3. **Análisis Histórico**: Analizar tendencias, volatilidad y estadísticas

## API Endpoints

- `GET /productos` - Listar todos
- `POST /productos` - Crear producto
- `PUT /productos/{id}` - Actualizar producto
- `DELETE /productos/{id}` - Eliminar producto

## Documentación API

FastAPI genera documentación automática en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del Proyecto
```
proyecto/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── database.db          # SQLite (se crea automático)
│   └── requirements.txt
└── frontend-angular/
    └── src/
        └── app/
            ├── app.component.ts      # Lógica
            ├── app.component.html    # Vista
            ├── app.component.css     # Estilos
            └── producto.service.ts   # Servicios API
```

## Solución de Problemas

**Error de conexión:**
- Verifica que ambos servidores estén corriendo
- Backend debe estar en puerto 8000
- Frontend debe estar en puerto 4200

**Error de CORS:**
- Asegúrate que `main.py` tenga configurado CORSMiddleware

**Campos vacíos al guardar:**
- Verifica que los inputs tengan el atributo `name`
