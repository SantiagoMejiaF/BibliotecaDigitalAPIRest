"""
Módulo principal de la aplicación Biblioteca Digital.

Este módulo define `app` como un paquete, permitiendo la correcta
importación y estructuración del código en toda la aplicación.

Estructura de la aplicación:
- `core/` → Configuración global, seguridad y base de datos.
- `models/` → Definición de modelos ORM con SQLAlchemy.
- `schemas/` → Esquemas de validación y serialización con Pydantic.
- `services/` → Lógica de negocio y manejo de datos.
- `api/` → Rutas y controladores de la API.
- `tests/` → Pruebas unitarias y de integración.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

# Permite que el directorio `app` sea tratado como un módulo de Python
