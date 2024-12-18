from flask import Flask, render_template
from infrastructure.web.routes import init_routes 
import locale

# Configura la localización para que los separadores de miles y demás formatos de números sean adecuados
locale.setlocale(locale.LC_ALL, '')

# Este filtro toma un valor y lo formatea como un número con separadores de miles.
def format_number(value):
    try:
        return locale.format_string("%d", value, grouping=True)
    except (ValueError, TypeError):
        return value  # Si hay un error, devuelve el valor sin cambios

# Crear la aplicación Flask
app = Flask(__name__, 
            template_folder='C:/Users/claud/Downloads/REFACT_PYTHON/infrastructure/templates',
            static_folder='C:/Users/claud/Downloads/REFACT_PYTHON/infrastructure/static')

# Configuración de la clave secreta para sesiones
app.secret_key = "mysecretkey_db"

# Inicializa las rutas
init_routes(app)

# Esto permite usar el filtro "format_number" directamente en las plantillas.
app.jinja_env.filters['format_number'] = format_number

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404 Not Found.html'), 404

# Ejecuta la aplicación Flask en modo de depuración para facilitar el desarrollo.
if __name__ == "__main__":
    app.run(debug=True)
