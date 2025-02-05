import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

UPLOAD_FOLDER = 'uploads'

def create_app() -> Flask:
    app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
    app.secret_key = "secret_key"

    instance_folder = os.path.join(os.getcwd(), 'instance')
    if not os.path.exists(instance_folder):
        os.makedirs(instance_folder)

    database_path = os.path.join(instance_folder, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    with app.app_context():
        from .models import Email, Note

        print("Sprawdzam i tworzę tabele w bazie (o ile ich brak)...")
        db.create_all()  
        print("Gotowe!")

    from .routes import main
    app.register_blueprint(main)
    
    return app
