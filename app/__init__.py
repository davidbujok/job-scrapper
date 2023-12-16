from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.jobs import jobs_bp
    app.register_blueprint(jobs_bp)
    from app.seed import seed
    app.cli.add_command(seed)

    return app




