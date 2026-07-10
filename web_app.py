import streamlit as st

from app.users import authenticate_user, initialize_users_db


st.set_page_config(
    page_title="AGENTE RAG",
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


def show_login() -> None:
    st.title("🤖 AGENTE PILON")
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
        st.rerun()

def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.user = None

    if "current_page" in st.session_state:
        del st.session_state.current_page

    st.rerun()

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
        st.title("💬 Chat")
        st.info("El chat se implementará en el siguiente paso.")

    elif current_page == "Documentos":
        st.title("📄 Documentos")
        st.info("La gestión de documentos se implementará próximamente.")

    elif current_page == "Usuarios":
        st.title("👥 Usuarios")
        st.info("La gestión de usuarios se implementará próximamente.")

def main() -> None:
    initialize_users_db()
    initialize_session()

    if not st.session_state.authenticated:
        show_login()
        return

    show_dashboard()


if __name__ == "__main__":
    main()