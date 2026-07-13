# 🤖 RAG Enterprise

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.59-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![Ollama](https://img.shields.io/badge/Ollama-LLM-black)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 📖 Descripción

**RAG Enterprise** es una aplicación web desarrollada en **Python** que implementa la arquitectura **Retrieval-Augmented Generation (RAG)** utilizando **LangChain**, **Ollama**, **ChromaDB** y **Streamlit**.

El sistema permite cargar documentos PDF, convertirlos en una base de conocimiento mediante embeddings y responder preguntas utilizando un modelo de lenguaje local, mostrando además las fuentes utilizadas para generar la respuesta.

Toda la aplicación cuenta con autenticación de usuarios, administración de documentos y gestión de roles.

---

# 🚀 Características

### 🤖 Inteligencia Artificial

- Arquitectura RAG
- Búsqueda semántica
- Embeddings con HuggingFace
- Ollama como LLM local
- Respuestas con fuentes
- Soporte para múltiples documentos PDF

---

### 🌐 Aplicación Web

- Login de usuarios
- Dashboard
- Chat con IA
- Historial de conversación
- Interfaz desarrollada en Streamlit

---

### 📄 Gestión Documental

- Cargar uno o varios PDF
- Visualizar documentos
- Eliminar documentos
- Reconstruir la base vectorial

---

### 👥 Administración

- Crear usuarios
- Roles Administrador / Usuario
- Activar usuarios
- Desactivar usuarios
- Contraseñas cifradas con bcrypt

---

# 🛠 Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| Python 3.12 | Lenguaje principal |
| Streamlit | Interfaz web |
| LangChain | Framework RAG |
| Ollama | Modelo LLM local |
| ChromaDB | Base vectorial |
| HuggingFace Embeddings | Embeddings |
| SQLite | Base de datos de usuarios |
| bcrypt | Encriptación de contraseñas |
| PyPDF | Lectura de documentos PDF |

---

# 🏗 Arquitectura

```
                    Usuario

                        │

                        ▼

                Streamlit (web_app.py)

                        │

                        ▼

                    ask.py

                        │

                        ▼

                  search.py

                        │

                        ▼

                  ChromaDB

                        │

                        ▼

                    Ollama

                        │

                        ▼

                  Respuesta
```

---

# 📂 Estructura del proyecto

```text
RAG-PYTHON/
│
├── app/
│   ├── __init__.py
│   ├── ask.py
│   ├── config.py
│   ├── create_vector_db.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── load_documents.py
│   ├── prompts.py
│   ├── search.py
│   └── users.py
│
├── data/
│   ├── chroma/
│   ├── documentos/
│   └── users.db
│
├── tests/
│
├── .env
├── .gitignore
├── create_admin.py
├── main.py
├── requirements.txt
├── web_app.py
└── README.md
```

---

# ⚙ Instalación

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/Rag-python.git

cd Rag-python
```

---

## 2️⃣ Crear entorno virtual

```bash
python -m venv venv
```

---

## 3️⃣ Activar entorno virtual

### Windows

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# 🤖 Instalar Ollama

Descargar desde

https://ollama.com

Luego descargar el modelo:

```bash
ollama pull llama3.2
```

Verificar instalación:

```bash
ollama run llama3.2
```

---

# 📄 Cargar documentos

Copiar los documentos PDF dentro de:

```
data/documentos
```

Luego reconstruir la base vectorial:

```bash
python -m app.create_vector_db
```

---

# 👤 Crear el primer administrador

```bash
python create_admin.py
```

Ingresar:

- Usuario
- Contraseña

---

# ▶ Ejecutar la aplicación

```bash
streamlit run web_app.py
```

---

# 💬 Funcionalidades

## Administrador

- Iniciar sesión
- Consultar documentos
- Cargar PDF
- Eliminar PDF
- Reconstruir la base vectorial
- Crear usuarios
- Activar usuarios
- Desactivar usuarios

---

## Usuario

- Iniciar sesión
- Consultar documentos
- Visualizar fuentes de información

---

# 📚 Flujo del sistema

```
Carga PDF

↓

Embeddings

↓

ChromaDB

↓

Pregunta del usuario

↓

Búsqueda semántica

↓

Ollama

↓

Respuesta + Fuentes
```

---

# 🔒 Seguridad

- Contraseñas cifradas con bcrypt
- Usuarios almacenados en SQLite
- Roles de acceso
- LLM ejecutado localmente mediante Ollama
- No se envían documentos a servicios externos

---

# 📌 Versiones

## ✅ v0.1.0

- Motor RAG
- LangChain
- ChromaDB
- Ollama
- Embeddings
- Respuestas con fuentes

---

## ✅ v0.2.0

- Interfaz web con Streamlit
- Login
- Dashboard
- Chat
- Gestión documental
- Administración de usuarios
- Roles
- Historial de conversación



---

# 👨‍💻 Autor

**Anthony Frank Uceda Alfaro**

Ingeniero de Sistemas

Proyecto desarrollado con fines educativos y de aprendizaje sobre Inteligencia Artificial Generativa, LangChain y sistemas RAG.

---

# ⭐ Si este proyecto te resulta útil...

¡No olvides darle una ⭐ al repositorio!