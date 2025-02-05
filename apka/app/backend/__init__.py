import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicjalizacja SQLAlchemy (jedna, wspólna instancja)
db = SQLAlchemy()

UPLOAD_FOLDER = 'uploads'

def create_app() -> Flask:
    app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
    app.secret_key = "secret_key"

    # Upewnij się, że mamy folder "instance" (jeśli nie istnieje, to go twórz)
    instance_folder = os.path.join(os.getcwd(), 'instance')
    if not os.path.exists(instance_folder):
        os.makedirs(instance_folder)

    # Konfiguracja ścieżki do pliku bazy w folderze instance
    database_path = os.path.join(instance_folder, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Inicjalizacja SQLAlchemy z aplikacją Flask
    db.init_app(app)

    with app.app_context():
        # Importujemy modele PRZED wywołaniem create_all()
        from .models import Email, Note

        print("Sprawdzam i tworzę tabele w bazie (o ile ich brak)...")
        db.create_all()  # Teraz SQLAlchemy zna klasy Email, Note
        print("Gotowe!")

    # Rejestrowanie blueprintu
    from .routes import main
    app.register_blueprint(main)
    
    return app
