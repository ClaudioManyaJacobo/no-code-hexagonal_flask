# run.py
from flask import Flask
from infrastructure.web.movie_controller import app
import locale

# Configura la localización para que los separadores de miles y demás formatos de números sean adecuados
locale.setlocale(locale.LC_ALL, '')

# Este filtro toma un valor y lo formatea como un número con separadores de miles.
def format_number(value):
    try:
        return locale.format_string("%d", value, grouping=True)
    except (ValueError, TypeError):
        return value  # Si hay un error, devuelve el valor sin cambios

# Esto permite usar el filtro "format_number" directamente en las plantillas.
app.jinja_env.filters['format_number'] = format_number

# Ejecuta la aplicación Flask en modo de depuración para facilitar el desarrollo.
if __name__ == "__main__":
    app.run(debug=True)
