from db import db

from config import Configuration


class PostModel(db.Model):
        __tablename__ = 'posts'

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(Configuration.MAX_TITLE_SIZE))
        body = db.Column(db.Text)
        user_id = db.Column(db.Integer, nullable=False)
        is_published = db.Column(db.Boolean, nullable=False)

        def __init__(self, *args, **kwargs):
            super(PostModel, self).__init__(*args, **kwargs)

        def __repr__(self):
            return "<Post id: {}, title: {}>".format(self.id, self.title)

        # @classmethod
        # def find_by_userid(cls, user_id):
        #     return cls.query.filter_by(username=user_id).first()

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
                    'user_id': self.user_id}

        def delete_from_db(self):
            db.session.delete(self)
            db.session.commit()
