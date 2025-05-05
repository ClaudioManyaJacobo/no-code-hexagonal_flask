# routes.py
from flask import render_template, request, redirect, url_for, session
from application.user.user_service import UserService
from infrastructure.web.movie_controller import index, show
from infrastructure.persistence.user_db_repository import UserApiRepository
from infrastructure.web.user_controller import UserController

# Crear las instancias necesarias
user_repository = UserApiRepository()  # Ya no se pasan credenciales aquí
user_service = UserService(user_repository)
user_controller = UserController(user_service)
from infrastructure.persistence.comment_db_repository import CommentDbRepository
from application.comment.comment_service import CommentService

def init_routes(app):
    # Ruta que muestra el formulario de inicio de sesión y maneja la autenticación
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return user_controller.login()

    # Ruta para crear usuario
    @app.route('/create_user', methods=['GET', 'POST'])
    def create_user():
        return user_controller.create_user()

    # Ruta para editar usuario
    @app.route('/edit_user', methods=['GET', 'POST'])
    def edit_user():
        return user_controller.edit_user()

    # Ruta para cerrar sesión
    @app.route('/logout')
    def logout():
        return user_controller.logout()
    
        # Configurar servicios adicionales
    comment_repository = CommentDbRepository()
    comment_service = CommentService(comment_repository)
    
    # Ruta para eliminar comentarios
    @app.route('/comment/delete/<int:comment_id>', methods=['POST'])
    def delete_comment(comment_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if comment_service.delete_comment(comment_id, session['user_id']):
            return redirect(request.referrer or url_for('index'))
        else:
            return "No se pudo eliminar el comentario", 403

    # Rutas relacionadas con películas
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/movie/<int:movie_id>', 'show', show, methods=['GET', 'POST'])
