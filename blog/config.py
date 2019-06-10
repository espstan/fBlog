import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = True
    # db settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'posts', 'blog.db')

    # post_params
    MAX_TITLE_SIZE = 140
