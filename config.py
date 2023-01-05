from os import environ

class Config:
    SECRET_KEY="#1523ABC"
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    TEMPLATE_FOLDER="./views/templates/"
    STATIC_FOLDER="./views/static/"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MAIL_SUBJECT_PREFIX='[Elvis Morales]'
    MAIL_SENDER='Elvis Morales <cristopherelvism@gmail.com>'
    MORALES_ADMIN=environ.get('MORALES_ADMIN')
    # @staticmethod
    # def init_app(app):
    #     pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:admin@localhost/authflask'
    MAIL_SERVER='smt.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=environ.get('MAIL_PASSWORD')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:admin@localhost/authflask'

class ProductionConfig(Config):
    pass

config = {
 'development': DevelopmentConfig,
 'testing': TestingConfig,
 'production': ProductionConfig,
 'default': DevelopmentConfig
}
