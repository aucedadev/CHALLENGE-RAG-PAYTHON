from getpass import getpass

from app.users import create_user, initialize_users_db


def main() -> None:
    initialize_users_db()

    username = input("Usuario administrador: ").strip()
    password = getpass("Contraseña: ")
    confirm_password = getpass("Confirma la contraseña: ")

    if password != confirm_password:
        print("Las contraseñas no coinciden.")
        return

    created = create_user(
        username=username,
        password=password,
        role="admin",
    )

    if created:
        print("Administrador creado correctamente.")
    else:
        print("Ese nombre de usuario ya existe.")


if __name__ == "__main__":
    main()