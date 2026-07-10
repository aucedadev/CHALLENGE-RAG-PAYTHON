import streamlit as st

from app.ask import ask_question
from app.users import authenticate_user, initialize_users_db


st.set_page_config(
    page_title="RAG Enterprise",
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
    st.title("🤖 RAG Enterprise")
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
    st.title("Agente Pilon ")
    st.caption(
        "Haz preguntas relacionados a la empresa TDV"
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


def show_dashboard() -> None:
    user = st.session_state.user

    with st.sidebar:
        st.title("🤖 RAG Enterprise")
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
        st.title("📄 Documentos")
        st.info(
            "La gestión de documentos se implementará "
            "en el siguiente paso."
        )

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