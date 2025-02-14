"""
Módulo de inicialización de los modelos de la base de datos.

Este archivo importa todas las entidades definidas en la carpeta `models`
para que puedan ser utilizadas en otras partes del proyecto sin necesidad
de importarlas individualmente.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.session import SessionToken
from app.models.role import Role
