from flask import Flask
from config import Config,config
from .models.user import db,login_manager
from flask_wtf.csrf import CSRFProtect 
from flask_migrate import Migrate
# from flask_login import LoginManager

csrf=CSRFProtect()
migrate=Migrate()
# login_manager=LoginManager()
# login_manager.session_protection='strong'
# login_manager.login_view='auth.login'

def create_app(config_name):
    app=Flask(__name__,static_folder=Config.STATIC_FOLDER,template_folder=Config.TEMPLATE_FOLDER)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app) 
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app,db)
    from .routes.login import auth
    app.register_blueprint(auth, url_prefix="/")
    return app


