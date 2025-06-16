from flask import Flask, render_template, redirect, url_for
import locale
from infrastructure.routes.user_routes import user_bp
from infrastructure.routes.movie_routes import movie_bp
from infrastructure.routes.comment_routes import comment_bp

# Configura la localización para que los separadores de miles y demás formatos de números sean adecuados
locale.setlocale(locale.LC_ALL, '')

# Este filtro toma un valor y lo formatea como un número con separadores de miles.
def format_number(value):
    try:
        return locale.format_string("%d", value, grouping=True)
    except (ValueError, TypeError):
        return value 

# Crear la aplicación Flask
app = Flask(__name__,
            template_folder='infrastructure/web/templates',
            static_folder='infrastructure/web/static')

# Configuración de la clave secreta para sesiones
app.secret_key = "type-198"

# Inicializa las rutas
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(movie_bp, url_prefix='/movie')
app.register_blueprint(comment_bp, url_prefix='/comment')

@app.route('/')
def root():
    return redirect(url_for('movie.index'))

# Esto permite usar el filtro "format_number" directamente en las plantillas.
app.jinja_env.filters['format_number'] = format_number

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404 Not Found.html'), 404

# Ejecuta la aplicación Flask en modo de depuración para facilitar el desarrollo.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
