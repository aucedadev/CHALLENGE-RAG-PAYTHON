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


def show_dashboard() -> None:
    user = st.session_state.user

    st.title("🤖 Bienvenido al AGENTE PILON")
    st.success(f"Sesión iniciada como: {user['username']}")
    st.write(f"Rol: **{user['role']}**")

    st.info("El inicio de sesión funciona correctamente.")

    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()


def main() -> None:
    initialize_users_db()
    initialize_session()

    if not st.session_state.authenticated:
        show_login()
        return

    show_dashboard()


if __name__ == "__main__":
    main()