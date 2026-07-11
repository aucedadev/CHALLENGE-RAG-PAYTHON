import streamlit as st
from pathlib import Path

from app.config import DOCUMENTS_DIR
from app.create_vector_db import create_vector_db

from app.ask import ask_question
from app.users import authenticate_user, initialize_users_db


st.set_page_config(
    page_title="BimBam Buy",
    page_icon="🤖",
    layout="centered",
)


def initialize_session() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Inicio"

    if "messages" not in st.session_state:
        st.session_state.messages = []


def show_login() -> None:
    st.title("🤖 RAG BimBam Buy")
    st.subheader("Inicio de sesión")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        submitted = st.form_submit_button(
            "Iniciar sesión",
            use_container_width=True,
        )

    if submitted:
        user = authenticate_user(username, password)

        if user is None:
            st.error("Usuario o contraseña incorrectos.")
            return

        st.session_state.authenticated = True
        st.session_state.user = user
        st.session_state.current_page = "Inicio"
        st.rerun()


def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.messages = []

    if "current_page" in st.session_state:
        del st.session_state.current_page

    st.rerun()


def show_chat() -> None:
    st.title("Agente BimBam Buy ")
    st.caption(
        "Haz preguntas relacionados a la empresa "
        "en los documentos PDF cargados."
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Escribe tu pregunta")

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Buscando información..."):
            try:
                response = ask_question(question)
                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as error:
                st.error(
                    "Ocurrió un error al consultar los documentos."
                )
                st.exception(error)

def show_documents() -> None:
    st.title("📄 Documentos")
    st.caption("Carga archivos PDF y actualiza la base de conocimiento.")

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    st.subheader("Documentos cargados")

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if pdf_files:
        for pdf_file in pdf_files:
            st.write(f"📄 {pdf_file.name}")
    else:
        st.info("Todavía no hay documentos PDF cargados.")

    st.divider()

    st.subheader("Cargar nuevos documentos")

    uploaded_files = st.file_uploader(
        "Selecciona uno o varios archivos PDF",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button(
        "Guardar documentos",
        use_container_width=True,
        disabled=not uploaded_files,
    ):
        saved_files = []

        for uploaded_file in uploaded_files:
            safe_filename = Path(uploaded_file.name).name
            destination = DOCUMENTS_DIR / safe_filename

            with open(destination, "wb") as file:
                file.write(uploaded_file.getbuffer())

            saved_files.append(safe_filename)

        st.success(
            f"Se guardaron {len(saved_files)} documento(s) correctamente."
        )

        for filename in saved_files:
            st.write(f"✅ {filename}")

    st.divider()

    st.subheader("Actualizar base vectorial")
    st.warning(
        "Este proceso vuelve a procesar todos los PDF y puede tardar "
        "varios minutos."
    )

    if st.button(
        "Reconstruir base vectorial",
        use_container_width=True,
    ):
        with st.spinner("Procesando documentos y creando embeddings..."):
            try:
                create_vector_db()
                st.success("Base vectorial actualizada correctamente.")
            except Exception as error:
                st.error("No se pudo actualizar la base vectorial.")
                st.exception(error)

def show_dashboard() -> None:
    user = st.session_state.user

    with st.sidebar:
        st.title("🤖 RAG BimBam Buy")
        st.write(f"Usuario: **{user['username']}**")
        st.write(f"Rol: **{user['role']}**")
        st.divider()

        menu_options = ["Inicio", "Chat"]

        if user["role"] == "admin":
            menu_options.extend(["Documentos", "Usuarios"])

        current_page = st.radio(
            "Menú",
            menu_options,
            key="current_page",
        )

        st.divider()

        if st.button(
            "Cerrar sesión",
            use_container_width=True,
        ):
            logout()

    if current_page == "Inicio":
        st.title("Panel principal")
        st.success(f"Bienvenido, {user['username']}.")

        if user["role"] == "admin":
            st.write(
                "Desde este panel podrás consultar documentos, "
                "cargar archivos PDF y administrar usuarios."
            )
        else:
            st.write(
                "Desde este panel podrás consultar la información "
                "disponible en los documentos."
            )

    elif current_page == "Chat":
        show_chat()

    elif current_page == "Documentos":
        show_documents()
    elif current_page == "Usuarios":
        st.title("👥 Usuarios")
        st.info(
            "La gestión de usuarios se implementará "
            "en un siguiente paso."
        )


def main() -> None:
    initialize_users_db()
    initialize_session()

    if not st.session_state.authenticated:
        show_login()
        return

    show_dashboard()


if __name__ == "__main__":
    main()