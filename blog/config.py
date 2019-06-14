import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = True
    # db settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
    # post_params
    MAX_POST_TITLE_SIZE = 140
    MAX_TAG_NAME_SIZE = 40

