from sqlalchemy.sql.functions import current_timestamp

from app import db

from config import Configuration


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(str(Configuration.MAX_TITLE_SIZE)))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=current_timestamp())
    is_published = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Post id: {}, title: {}>".format(self.id, self.title)
