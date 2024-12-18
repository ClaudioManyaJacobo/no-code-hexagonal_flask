# routes.py
from flask import render_template, request, redirect, url_for, session, make_response
from application.user.user_service import UserService
from infrastructure.web.movie_controller import index, show
from infrastructure.persistence.user_api_repository import UserApiRepository
from infrastructure.web.user_controller import UserController

# Configuración de la API y del repositorio de usuarios
user_repository = UserApiRepository(server="172.22.15.132", user="sa", password="GrupoHexagonal#0112", database="Users")
user_service = UserService(user_repository)
user_controller = UserController(user_service)

def init_routes(app):
    # Ruta que muestra el formulario de inicio de sesión y maneja la autenticación
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return user_controller.login()

    # Rutas para crear y editar usuarios
    @app.route('/create_user', methods=['GET', 'POST'])
    def create_user():
        return user_controller.create_user()

    @app.route('/edit_user', methods=['GET', 'POST'])
    def edit_user():
        return user_controller.edit_user()

    # Ruta para cerrar sesión
    @app.route('/logout')
    def logout():
        return user_controller.logout()

    # Rutas relacionadas con las películas
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/movie/<int:movie_id>', 'show', show)
