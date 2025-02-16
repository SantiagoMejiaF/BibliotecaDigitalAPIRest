# 📚 Biblioteca Digital API

API REST desarrollada con **FastAPI** para gestionar una biblioteca digital, permitiendo la administración de usuarios, libros y préstamos.

---

## 🚀 Instalación y Configuración

### 1️⃣ Clonar el Repositorio
```sh
git clone https://github.com/SantiagoMejiaF/BibliotecaDigitalAPIRest.git
cd BibliotecaDigitalAPIRest
```

### 2️⃣ Crear un Entorno Virtual y Activarlo
```sh
python -m venv .venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias
```sh
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
DATABASE_URL=postgresql://user:password@localhost:5432/BibliotecaDigitalAPI
SECRET_KEY=your_secret_key_here
```

### 5️⃣ Ejecutar la API
```sh
uvicorn app.main:app --port 3280 --reload
```

La API estará disponible en: [http://127.0.0.1:3280](http://127.0.0.1:3280)

Accede a la documentación interactiva en:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:3280/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:3280/redoc)

---

## Endpoints
### Usuarios
- `POST /usuarios/` - Crear un usuario
- `GET /usuarios/{id}` - Obtener un usuario por ID
- `PUT /usuarios/{id}` - Actualizar un usuario
- `DELETE /usuarios/{id}` - Eliminar un usuario

### Autores
- `POST /autores/` - Crear un autor
- `GET /autores/{id}` - Obtener un autor por ID
- `PUT /autores/{id}` - Actualizar un autor
- `DELETE /autores/{id}` - Eliminar un autor

### Libros
- `POST /libros/` - Crear un libro
- `GET /libros/{id}` - Obtener un libro por ID
- `PUT /libros/{id}` - Actualizar un libro
- `DELETE /libros/{id}` - Eliminar un libro
- `GET /libros/buscar/` - Buscar libros por título, autor o año de publicación
- `POST /libros/prestamo/{id}` - Registrar un préstamo
- `POST /libros/devolucion/{id}` - Registrar una devolución

---

## Pruebas
Ejecuta las pruebas con:
```sh
pytest --cov=app --cov-report=term-missing
```
Se debe garantizar una cobertura mínima del 80% e incluir mocks en los test.

---

## Contribuir
1. Haz un **fork** del repositorio.
2. Crea una **rama** (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza **commits** (`git commit -m 'Agrega nueva funcionalidad'`).
4. Sube los cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un **pull request**.

---

## Licencia
Este proyecto está bajo la licencia MIT. Puedes consultarla en el archivo [LICENSE](LICENSE).

---

## Contacto
Para cualquier duda o sugerencia, contacta a:
📧 Email: santiagomejia2000@hotmail.com
💼 LinkedIn: https://www.linkedin.com/in/santiago-mej%C3%ADa-fern%C3%A1ndez-a370a1235/

