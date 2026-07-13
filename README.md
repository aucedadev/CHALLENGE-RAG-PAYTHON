# 🤖 RAG Enterprise

Sistema RAG (Retrieval-Augmented Generation) desarrollado con Python, LangChain, Ollama, ChromaDB y Streamlit.

Permite consultar información almacenada en documentos PDF mediante inteligencia artificial, administrando usuarios, documentos y consultas desde una interfaz web.

---

# 🚀 Características

- Autenticación de usuarios
- Roles (Administrador / Usuario)
- Chat con IA utilizando Ollama
- Recuperación semántica mediante ChromaDB
- Soporte para múltiples documentos PDF
- Gestión de documentos desde la interfaz web
- Creación y administración de usuarios
- Respuestas con fuentes de información
- Interfaz desarrollada con Streamlit

---

# 🛠 Tecnologías

- Python 3.12
- LangChain
- Ollama
- ChromaDB
- HuggingFace Embeddings
- Streamlit
- SQLite
- bcrypt

---

# 📁 Arquitectura

```
RAG-PYTHON/
│
├── app/
│   ├── ask.py
│   ├── config.py
│   ├── create_vector_db.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── prompts.py
│   ├── search.py
│   ├── users.py
│   └── ...
│
├── data/
│   ├── chroma/
│   ├── documentos/
│   └── users.db
│
├── web_app.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙ Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Rag-python
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

## 3. Activar entorno

Windows

```powershell
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# 🤖 Instalar Ollama

Instalar Ollama desde:

https://ollama.com

Descargar el modelo:

```bash
ollama pull llama3.2
```

---

# 📄 Cargar documentos

Copiar los PDF dentro de:

```
data/documentos/
```

Actualizar la base vectorial:

```bash
python -m app.create_vector_db
```

---

# 👤 Crear administrador

```bash
python create_admin.py
```

---

# 🌐 Ejecutar la aplicación

```bash
streamlit run web_app.py
```

---

# 💬 Uso

Administrador

- Crear usuarios
- Activar usuarios
- Desactivar usuarios
- Cargar documentos
- Eliminar documentos
- Reconstruir la base vectorial

Usuario

- Iniciar sesión
- Consultar documentos mediante IA
- Visualizar fuentes utilizadas

---

# 📌 Estado del proyecto

Versión actual

```
v0.2.0
```

Proyecto funcional.

---

# 📄 Licencia

Proyecto desarrollado con fines educativos y de aprendizaje.