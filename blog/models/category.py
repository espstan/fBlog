from db import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Category id: {}, name: {}>'.format(self.id, self.name)
