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


class PostList(Resource):
    def get(self):
        return {'posts': [post.get_json() for post in PostModel.query.all()]}


class PostStatistics(Resource):
    def get(self):
        print(sum(1 for post in PostModel.query.all() if post.is_published))
        return {'posts': len(list(PostModel.query.all())),
                'published posts': sum(1 for post in PostModel.query.all() if post.is_published),
                'drafts': sum(1 for post in PostModel.query.all() if not post.is_published)}
