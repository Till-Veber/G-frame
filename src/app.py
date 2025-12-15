from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from src.models.base import db
from src.models.user import User
from flask import send_from_directory
import os

login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя по ID для Flask-Login"""
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('src.config.Config')

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'

    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
    CHARTS_DIR = os.path.join(PROJECT_ROOT, 'data', 'img', 'charts')

    @app.route('/charts/<path:filename>')
    def serve_chart(filename):
        filepath = os.path.join(CHARTS_DIR, filename)
        if not os.path.exists(filepath):
            return "Файл не найден", 404
        return send_from_directory(CHARTS_DIR, filename)

    with app.app_context():
        from src.routes.main import bp as main_bp
        from src.routes.auth import bp as auth_bp
        from src.routes.builds import bp as builds_bp
        from src.routes.experiments import bp as experiments_bp
        from src.routes.user import bp as user_bp

        # Регистрация Blueprint'ов
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(builds_bp, url_prefix='/builds')
        app.register_blueprint(experiments_bp, url_prefix='/exp')
        app.register_blueprint(user_bp, url_prefix='/user')

        # Создание таблиц
        db.create_all()

        return app