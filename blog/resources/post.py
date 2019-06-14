from flask import request

from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.post import PostModel


class PostRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    parser.add_argument('body',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help='This field cannot be blank.')

    parser.add_argument('is_published',
                        type=bool,
                        required=True,
                        help='This field cannot be blank.')

    def post(self):
        data = PostRegister.parser.parse_args()
        if len(data['title']) > Configuration.MAX_TITLE_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_TITLE_SIZE)}
        new_post = PostModel(**data)
        try:
            new_post.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return new_post.get_json(), 201


class Post(Resource):
    def delete(self, _id):
        if str(_id).isdigit():
            post = PostModel.find_by_id(_id)
            if post:
                try:
                    post.delete_from_db()
                except SQLAlchemyError as e:
                    err = str(e.__class__.__name__)
                    return {'message': '{}'.format(err)}, 500
                return {'message': 'Post was deleted'}
            return {'message': 'Post with id={} was not found'.format(_id)}
        return {'message': 'id must be a number'}




class PostList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help='This field cannot be blank.')
    def get(self):
        return {'posts': [post.get_json() for post in PostModel.query.all()]}

    def delete(self):
        data = PostList.parser.parse_args()
        for post in data:
            Post.delete(post)


class PostStatistics(Resource):
    def get(self):
        return {'posts': PostModel.query.all().count(),
                'published posts': PostModel.query.filter_by(is_published=True).all().count(),
                'drafts': PostModel.query.filter_by(is_published=False).all().count()}

        # return {'posts': len(list(PostModel.query.all())),
        #         'published posts': sum(1 for post in PostModel.query.all() if post.is_published),
        #         'drafts': sum(1 for post in PostModel.query.all() if not post.is_published)}
