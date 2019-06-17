from db import db

from config import Configuration

from models.post import PostModel as PM


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(Configuration.MAX_COMMENT_NAME_SIZE))
    body = db.Column(db.Text)
    email = db.Column(db.String(Configuration.MAX_EMAIL_ADDRESS_SIZE))
    post_id = db.Column('post_id', db.Integer, db.ForeignKey(PM.id))

    def __init__(self, *args, **kwargs):
        super(CommentModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Comment id: {}, name: {}>".format(self.id, self.name)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_json(self):
        return {'id': self.id,
                'name': self.name,
                'body': self.body,
                'post_id': self.post_id}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
