from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.tag import TagModel as TM


class Tag(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    def post(self):
        data = Tag.parser.parse_args()
        name = data['name']

        if len(name) > Configuration.MAX_TAG_NAME_SIZE:
            return {'message': 'A name\'s length is more than {}'.format(Configuration.MAX_TAG_NAME_SIZE)}

        if TM.query.filter(TM.name == name).first():
            return {'message': 'Tag \'{}\' already exists'.format(name)}

        tag = TM(name=name)
        try:
            tag.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return tag.get_json(), 201

    def put(self):
        data = Tag.parser.parse_args()
        name = data['name']

        if len(name) > Configuration.MAX_TAG_NAME_SIZE:
            return {'message': 'A tag\'s length is more than {}'.format(Configuration.MAX_TAG_NAME_SIZE)}

        tag = TM.find_by_name(name)
        if not tag:
            tag = TM(name=name)
        else:
            if not TM.query.filter(TM.name == name).first():
                tag.name = name
            else:
                return {'message': 'Tag name \'{}\' already exists'.format(data['name'])}

        try:
            tag.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return tag.get_json(), 201

    def delete(self):
        data = Tag.parser.parse_args()
        name = data['name']
        tag = TM.find_by_name(name)
        if tag:
            try:
                tag.delete_from_db()
            except SQLAlchemyError as e:
                err = str(e.__class__.__name__)
                return {'message': '{}'.format(err)}, 500
            return {'message': 'Tag was deleted'}
        return {'message': 'Tag with name: \'{}\' was not found'.format(name)}


class TagList(Resource):
    def get(self):
        return {'tags': [tag.get_json() for tag in TM.query.all()]}
