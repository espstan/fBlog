from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.category import CategoryModel as CM

from models.post import PostModel as PM


def get_posts(posts_id):
    posts = []
    for _id in posts_id:
        post = PM.find_by_id(_id)
        if post:
            posts.append(post)
        else:
            return {'message': 'There is no such post: \'{}\''.format(_id)}
    return posts


def add_posts(new_category, posts):
    for post in set(posts):
        if PM.query.filter(PM.id == post.id).first():
            new_category.posts.append(post)
        else:
            return {'message': 'There is no such post: \'{}\''.format(post.id)}
    return new_category


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('posts',
                        type=int,
                        action='append',
                        required=False)

    def post(self, name):
        if name:
            if CM.find_by_name(name):
                return {'message': 'A category with name \'{}\' already exists'.format(name)}, 400

        if len(name) > Configuration.MAX_CATEGORY_NAME_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_CATEGORY_NAME_SIZE)}

        data = Category.parser.parse_args()
        posts_id = data['posts']
        if posts_id:
            posts = get_posts(posts_id)
        else:
            posts = []

        category = CM(name=name)
        if posts:
            category = add_posts(category, posts)
        try:
            category.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return category.get_json(), 201

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
        if posts_id:
            posts = get_posts(posts_id)
        else:
            posts = []

        category = CM.find_by_name(name)
        if not category:
            category = CM(name=name)
        else:
            category.name = name

        category.posts = []

        if posts:
            category = add_posts(category, posts)

        try:
            category.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return category.get_json(), 201


class CategoryList(Resource):
    def get(self):
        return {'categories': [category.get_json() for category in CM.query.all()]}
