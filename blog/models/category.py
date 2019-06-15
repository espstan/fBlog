from db import db

from config import Configuration

# from models.post import PostModel


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(Configuration.MAX_CATEGORY_NAME_SIZE),
                     unique=True)
    post = db.relationship('models.post.PostModel',
                           backref='categories',
                           lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(CategoryModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Category id: {}, name: {}>'.format(self.id, self.name)
