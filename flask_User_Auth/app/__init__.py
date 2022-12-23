from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect 
app=Flask(__name__,static_folder=Config.STATIC_FOLDER,template_folder=Config.TEMPLATE_FOLDER)
app.config.from_object(Config)

csrf=CSRFProtect(app)
db=SQLAlchemy(app)