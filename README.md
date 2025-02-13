# 📚 Biblioteca Digital API

API REST desarrollada con **FastAPI** para gestionar una biblioteca digital, permitiendo la administración de usuarios, libros y préstamos.

## 🚀 Instalación y Configuración

### 1️⃣ Clonar el Repositorio
```sh
git clone https://github.com/tu-usuario/biblioteca-api.git
cd biblioteca-api

### 2️⃣ Crear un Entorno Virtual y Activarlo
```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3️⃣ Instalar Dependencias
```sh
pip install -r requirements.txt

4️⃣ Configurar Variables de Entorno
Crear un archivo .env con el siguiente contenido:
DATABASE_URL=postgresql://user:password@localhost:5432/biblioteca_db
SECRET_KEY=your_secret_key_here

5️⃣ Ejecutar la API
uvicorn app.main:app --reload

La API estará disponible en: http://127.0.0.1:8000