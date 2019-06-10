import os


class Configuration(object):
    DEBUG = True
    # db settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'posts', 'blog.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'posts', 'migrations')

    # post_params
    MAX_TITLE_SIZE = 140
