# Importamos la aplicación
from app import create_app
import os

# Instanciamos la app
app = create_app()
# Para guardar los archivos pdf
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/docs')

# Corre la aplicación por el puerto 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)
