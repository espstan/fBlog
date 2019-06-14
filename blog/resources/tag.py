from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.tag import TagModel


class TagRegister(Resource):
    def post(self, name):
        if len(name) > Configuration.MAX_TAG_NAME_SIZE:
            return {'message': 'A name\'s length is more than {}'.format(Configuration.MAX_TAG_NAME_SIZE)}

        if name in TagModel.get_tags():
            return {'message': 'Tag name already exists'}

        new_tag = TagModel(name)
        try:
            new_tag.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return new_tag.get_json(), 201

    def get(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass


class TagList(Resource):
    def get(self):
        return {'tags': [tag.get_json() for tag in TagModel.query.all()]}
