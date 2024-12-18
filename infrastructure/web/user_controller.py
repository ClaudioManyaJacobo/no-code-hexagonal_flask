# user_controller.py
from flask import request, render_template, redirect, url_for, jsonify, session
from application.user.user_service import UserService

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    # Método para iniciar sesión controlador
    def login(self):
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")

            user = self.user_service.authenticate_user(email, password)
            if user:
                session['user_id'] = user.user_id
                session['username'] = user.name
                # Redirigir después de un pequeño retraso sin recargar la página
                return render_template('user/login.html', success_message="Comprobando...")
            else:
                # Mostrar solo el mensaje de error sin redirigir
                return render_template('user/login.html', error_message="Credenciales inválidas")
        
        return render_template('user/login.html')


    # Método para crear un usuario
    def create_user(self):
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            # Verifica si el correo ya está registrado
            if self.user_service.get_user_by_email(email):
                return render_template('user/create_user.html', error="El correo electrónico ya está registrado.")
            
            # Si el correo no está registrado, lo crea
            self.user_service.create_user(name, email, password)
            return redirect(url_for('login')) 

        return render_template('user/create_user.html')

    # Método para editar un usuario
    def edit_user(self):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        user = self.user_service.get_user_by_id(user_id)

        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            self.user_service.update_user(user_id, name, password)
            session['username'] = name  
            return redirect(url_for('index'))

    # Método para cerrar sesión
    def logout(self):
        session.pop('user_id', None)
        return redirect(url_for('login'))
