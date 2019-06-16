from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.category import CategoryModel


class Category(Resource):
    def post(self, name):
        if name:
            if CategoryModel.find_by_name(name):
                return {'message': 'An item with name \'{}\' already exists'.format(name)}, 400

        if len(name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        new_category = CategoryModel(name=name)

        try:
            new_category.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return new_category.get_json(), 201

    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            try:
                category.delete_from_db()
            except SQLAlchemyError as e:
                err = str(e.__class__.__name__)
                return {'message': '{}'.format(err)}, 500
            return {'message': 'Category was deleted'}
        return {'message': 'Category with name={} was not found'.format(name)}


class CategoryList(Resource):
    def get(self):
        return {'categories': [category.get_json() for category in CategoryModel.query.all()]}