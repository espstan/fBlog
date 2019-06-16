from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.category import CategoryModel as CM


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    def post(self, name):
        if name:
            if CM.find_by_name(name):
                return {'message': 'A category with name \'{}\' already exists'.format(name)}, 400

        if len(name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        new_category = CM(name=name)

        try:
            new_category.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return new_category.get_json(), 201

    def delete(self, name):
        category = CM.find_by_name(name)
        if category:
            try:
                category.delete_from_db()
            except SQLAlchemyError as e:
                err = str(e.__class__.__name__)
                return {'message': '{}'.format(err)}, 500
            return {'message': 'Category was deleted'}
        return {'message': 'Category with name={} was not found'.format(name)}

    def put(self, name):
        data = Category.parser.parse_args()
        new_name = data['name']

        if len(name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A name\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        if len(new_name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A name\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        if CM.find_by_name(new_name):
            return {'message': 'A category with name \'{}\' already exists'.format(new_name)}, 400

        if name:
            category = CM.find_by_name(name)
            if category:
                category.name = new_name
                try:
                    category.save_to_db()
                except SQLAlchemyError as e:
                    err = str(e.__class__.__name__)
                    return {'message': '{}'.format(err)}, 500
                return category.get_json(), 201
            else:
                return {'message': 'No such category: \'{}\''.format(name)}, 400
        else:
            return {'message': 'Incorrect category\'s name: {}'.format(name)}


class CategoryList(Resource):
    def get(self):
        return {'categories': [category.get_json() for category in CM.query.all()]}
