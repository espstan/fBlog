from sqlalchemy.sql.functions import current_timestamp

from app import db

from config import Configuration


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(Configuration.MAX_TITLE_SIZE))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=current_timestamp())
    is_published = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Post id: {}, title: {}>".format(self.id, self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    email = db.Column(db.String(254))
    body = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comment id: {}, name: {}>'.format(self.id, self.name)
