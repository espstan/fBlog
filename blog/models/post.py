from sqlalchemy.ext.declarative import declarative_base

from config import Configuration

from db import db

from models.tag import TagModel

from models.category import CategoryModel

post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey(TagModel.id))
                     )


class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True)

    title = db.Column(db.String(Configuration.MAX_POST_TITLE_SIZE))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer,
                        nullable=False)
    is_published = db.Column(db.Boolean,
                             nullable=False)
    tags = db.relationship('TagModel',
                           secondary=post_tags,
                           backref=db.backref('posts'),
                           lazy='dynamic')
    category_id = db.Column('category_id',
                            db.Integer,
                            db.ForeignKey(CategoryModel.id))

    def __init__(self, *args, **kwargs):
        super(PostModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Post id: {}, title: {}>".format(self.id, self.title)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_json(self):
        return {'id': self.id,
                'title': self.title,
                'body': self.body,
                'is_published': self.is_published,
                'user_id': self.user_id,
                # 'tags': self.tags,
                'category_id': self.category_id}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
