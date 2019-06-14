from db import db


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),
                     unique=True,
                     nullable=False)

    def __init__(self, *args, **kwargs):
        super(TagModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)

    def get_tags(self):
        return [tag for tag in TagModel.query.all()]
