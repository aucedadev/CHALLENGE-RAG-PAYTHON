import streamlit as st
from pathlib import Path

from app.config import DOCUMENTS_DIR
from app.create_vector_db import create_vector_db

from app.ask import ask_question
from app.users import (
    authenticate_user,
    create_user,
    initialize_users_db,
    list_users,
    set_user_active,
)


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
    if "document_to_delete" not in st.session_state:
        st.session_state.document_to_delete = None


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
            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(f"📄 {pdf_file.name}")

            with col2:
                if st.button(
                    "🗑️",
                    key=f"delete_{pdf_file.name}",
                    help=f"Eliminar {pdf_file.name}",
                ):
                    st.session_state.document_to_delete = pdf_file.name
    else:
        st.info("Todavía no hay documentos PDF cargados.")

    if st.session_state.document_to_delete:
        filename = st.session_state.document_to_delete

        st.warning(f"¿Seguro que deseas eliminar **{filename}**?")

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button(
                "Sí, eliminar",
                use_container_width=True,
                type="primary",
            ):
                file_path = DOCUMENTS_DIR / filename

                try:
                    file_path.unlink()
                    del st.session_state.document_to_delete

                    st.success(
                        f"El documento {filename} fue eliminado correctamente."
                    )
                    st.warning(
                        "Debes reconstruir la base vectorial para aplicar el cambio."
                    )
                    st.rerun()

                except FileNotFoundError:
                    st.error("El documento ya no existe.")
                    del st.session_state.document_to_delete

                except Exception as error:
                    st.error("No se pudo eliminar el documento.")
                    st.exception(error)

        with cancel_col:
            if st.button(
                "Cancelar",
                use_container_width=True,
            ):
                del st.session_state.document_to_delete
                st.rerun()

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

def show_users() -> None:
    st.title("👥 Administración de usuarios")
    st.caption("Crea usuarios y controla su acceso al sistema.")

    current_user = st.session_state.user

    st.subheader("Crear usuario")

    with st.form("create_user_form", clear_on_submit=True):
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")
        confirm_password = st.text_input(
            "Confirmar contraseña",
            type="password",
        )
        role = st.selectbox(
            "Rol",
            options=["user", "admin"],
            format_func=lambda value: (
                "Usuario" if value == "user" else "Administrador"
            ),
        )

        submitted = st.form_submit_button(
            "Crear usuario",
            use_container_width=True,
        )

    if submitted:
        if not username.strip():
            st.error("El nombre de usuario es obligatorio.")

        elif not password:
            st.error("La contraseña es obligatoria.")

        elif password != confirm_password:
            st.error("Las contraseñas no coinciden.")

        elif len(password) < 6:
            st.error("La contraseña debe tener al menos 6 caracteres.")

        else:
            try:
                created = create_user(
                    username=username,
                    password=password,
                    role=role,
                )

                if created:
                    st.success("Usuario creado correctamente.")
                    st.rerun()
                else:
                    st.error("Ese nombre de usuario ya existe.")

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error("No se pudo crear el usuario.")
                st.exception(error)

    st.divider()
    st.subheader("Usuarios registrados")

    users = list_users()

    if not users:
        st.info("No hay usuarios registrados.")
        return

    for user in users:
        information_column, action_column = st.columns([4, 2])

        with information_column:
            status = "🟢 Activo" if user["is_active"] else "🔴 Inactivo"
            role_name = (
                "Administrador"
                if user["role"] == "admin"
                else "Usuario"
            )

            st.markdown(f"**{user['username']}**")
            st.write(f"Rol: {role_name}")
            st.write(f"Estado: {status}")

        with action_column:
            is_current_user = user["id"] == current_user["id"]

            if is_current_user:
                st.info("Sesión actual")

            elif user["is_active"]:
                if st.button(
                    "Desactivar",
                    key=f"deactivate_user_{user['id']}",
                    use_container_width=True,
                ):
                    set_user_active(user["id"], False)
                    st.success(
                        f"El usuario {user['username']} fue desactivado."
                    )
                    st.rerun()

            else:
                if st.button(
                    "Activar",
                    key=f"activate_user_{user['id']}",
                    use_container_width=True,
                ):
                    set_user_active(user["id"], True)
                    st.success(
                        f"El usuario {user['username']} fue activado."
                    )
                    st.rerun()

        st.divider()
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
        show_users()


def main() -> None:
    initialize_users_db()
    initialize_session()

    if not st.session_state.authenticated:
        show_login()
        return

    show_dashboard()


if __name__ == "__main__":
    main()