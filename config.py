class Config:
    SECRET_KEY="#1523ABC"
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    TEMPLATE_FOLDER="./views/templates/"
    STATIC_FOLDER="./views/static/"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    # @staticmethod
    # def init_app(app):
    #     pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:admin@localhost/authflask'

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
