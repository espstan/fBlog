import os


class Configuration(object):
    DEBUG = True

    #db settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)

    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///', basedir, 'blog.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')


    print(SQLALCHEMY_DATABASE_URI)
    print(SQLALCHEMY_MIGRATE_REPO)


