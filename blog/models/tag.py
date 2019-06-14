from db import db

from config import Configuration


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(Configuration.MAX_TAG_NAME_SIZE),
                     unique=True,
                     nullable=False)

    def __init__(self, *args, **kwargs):
        super(TagModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)

    def get_tags(self):
        return [tag for tag in TagModel.query.all()]

    def get_json(self):
        return {'id': self.id,
                'name': self.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
