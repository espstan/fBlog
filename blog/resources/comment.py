from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.comment import CommentModel as CM

from models.post import PostModel as PM


class Comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    parser.add_argument('body',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    parser.add_argument('post_id',
                        type=int,
                        required=True,
                        help='This field cannot be blank.')

    def post(self, _id):
        data = Comment.parser.parse_args()

        if len(data['name']) > Configuration.MAX_COMMENT_NAME_SIZE:
            return {'message': 'A comment\'s name length is more than {}'.format(Configuration.MAX_COMMENT_NAME_SIZE)}

        if len(data['email']) > Configuration.MAX_EMAIL_ADDRESS_SIZE:
            return {'message': 'email\'s length is more than {}'.format(Configuration.MAX_EMAIL_ADDRESS_SIZE)}

        if not PM.find_by_id(data['post_id']):
            return {'message': 'There is no such post: \'{}\''.format(data['post_id'])}

        comment = CM(**data)
        try:
            comment.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return comment.get_json(), 201

    def put(self, name):
        pass

    def delete(self, name):
        pass


class CommentList(Resource):
    def get(self):
        return {'comments': [comment.get_json() for comment in CM.query.all()]}