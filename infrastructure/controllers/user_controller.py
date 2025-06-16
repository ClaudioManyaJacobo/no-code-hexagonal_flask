from flask import request, render_template, redirect, url_for, session, flash
import re
from application.user.user_service import UserService

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self):
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            user = self.user_service.authenticate_user(email, password)
            if user:
                session['user_id'] = user.user_id
                session['username'] = user.name
                return redirect(url_for('movie.index'))
            else:
                return render_template('user/login.html', error_message="Credenciales inválidas")
        return render_template('user/login.html')

    def register(self):
        if request.method == 'POST':
            name = request.form['name'].strip()
            email = request.form['email'].strip()
            password = request.form['password'].strip()

            # Validaciones
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.(com|net|org|edu|pe|es)$'
            password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=\-]).{8,}$'

            if not re.match(email_pattern, email):
                error = "Correo inválido o dominio no permitido (usa .com, .pe, .org, etc)."
                return render_template('user/create_user.html', error=error)

            if not re.match(password_pattern, password):
                error = "La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un símbolo."
                return render_template('user/create_user.html', error=error)

            if self.user_service.get_user_by_email(email):
                return render_template('user/create_user.html', error="El correo ya está registrado.")

            self.user_service.create_user(name, email, password)
            flash("¡Usuario registrado correctamente!", "success")
            return redirect(url_for('user.login'))
        return render_template('user/create_user.html')

    def edit(self):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))

        user_id = session['user_id']
        user = self.user_service.get_user_by_id(user_id)

        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            self.user_service.update_user(user_id, name, password)
            session['username'] = name
            return redirect(url_for('movie.index'))

        return render_template('user/edit_user.html', user=user)

    def logout(self):
        session.clear()
        return redirect(url_for('user.login'))
