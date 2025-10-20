# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

# Permitir peticiones desde Angular y Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos
class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    precio: float

# Conectar a SQLite
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla al iniciar
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# LISTAR todos
@app.get("/productos", response_model=List[dict])
def listar_productos():
    conn = get_db()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return [dict(p) for p in productos]

#OBTENER uno
@app.get("/productos/{id}")
def obtener_producto(id: int):
    conn = get_db()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return dict(producto)

#CREAR
@app.post("/productos", response_model=dict)
def crear_producto(producto: Producto):
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)',
        (producto.nombre, producto.descripcion, producto.precio)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {"id": nuevo_id, "mensaje": "Producto creado"}

#EDITAR
@app.put("/productos/{id}")
def editar_producto(id: int, producto: Producto):
    conn = get_db()
    cursor = conn.execute(
        'UPDATE productos SET nombre=?, descripcion=?, precio=? WHERE id=?',
        (producto.nombre, producto.descripcion, producto.precio, id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    conn.close()
    return {"mensaje": "Producto actualizado"}

#ELIMINAR
@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    conn = get_db()
    cursor = conn.execute('DELETE FROM productos WHERE id=?', (id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    conn.close()
    return {"mensaje": "Producto eliminado"}

# Para correr: uvicorn main:app --reload