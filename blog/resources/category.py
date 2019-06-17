from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.category import CategoryModel as CM

from models.post import PostModel as PM


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('posts',
                        type=int,
                        action='append',
                        required=True,
                        help='This field cannot be blank.')

    def post(self, name):
        if name:
            if CM.find_by_name(name):
                return {'message': 'A category with name \'{}\' already exists'.format(name)}, 400

        if len(name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        data = Category.parser.parse_args()
        posts_id = data['posts']
        posts = []
        for _id in posts_id:
            post = PM.find_by_id(_id)
            if post:
                posts.append(post)
            else:
                return {'message': 'There is no such post: \'{}\''.format(_id)}

        new_category = CM(name=name)

        for post in set(posts):
            if PM.query.filter(PM.id == post.id).first():
                new_category.posts.append(post)
            else:
                return {'message': 'There is no such post: \'{}\''.format(post.id)}
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
        return {'message': 'Category with name: \'{}\' was not found'.format(name)}

    def put(self, name):
        data = Category.parser.parse_args()

        if len(name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A name\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        posts_id = data['posts']
        posts = []
        for _id in posts_id:
            post = PM.find_by_id(_id)
            if post:
                posts.append(post)
            else:
                return {'message': 'There is no such post: \'{}\''.format(_id)}

        category = CM.find_by_name(name)
        if not category:
            category = CM(name=name)
        else:
            category.name = name

        category.posts = []
        for post in set(posts):
            if PM.query.filter(PM.id == post.id).first():
                category.posts.append(post)
            else:
                return {'message': 'There is no such post: \'{}\''.format(post.id)}

        try:
            category.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return category.get_json(), 201


class CategoryList(Resource):
    def get(self):
        return {'categories': [category.get_json() for category in CM.query.all()]}
