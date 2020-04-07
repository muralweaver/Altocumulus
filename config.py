# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config(object):
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     SECRET_KEY = 'this-really-needs-to-be-changed'
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


# class ProductionConfig(Config):
#     DEBUG = False


# class StagingConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class DevelopmentConfig():
#     DEBUG = True
#     DEVELOPMENT = True
#     # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class TestingConfig(Config):
#     DEBUG = True
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
#     PRESERVE_CONTEXT_ON_EXCEPTION = False
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    