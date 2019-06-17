from db import db

from config import Configuration


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(Configuration.MAX_CATEGORY_NAME_SIZE),
                     unique=True)
    posts = db.relationship('models.post.PostModel',
                           backref=db.backref('categories'),
                           lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(CategoryModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Category id: {}, name: {}>'.format(self.id, self.name)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_json(self):
        return {'id': self.id,
                'name': self.name,
                'posts': self.get_posts()}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_posts(self):
        return [post.id for post in self.posts]
