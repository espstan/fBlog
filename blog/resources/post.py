from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.post import PostModel

from models.tag import TagModel


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

    parser.add_argument('tags',
                        type=list,
                        required=True,
                        help='This field cannot be blank.')

    def post(self):
        data = PostRegister.parser.parse_args()
        if len(data['title']) > Configuration.MAX_TITLE_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_TITLE_SIZE)}

        for tag in data['tags']:
            if tag.name not in TagModel.get_tags():
                return {'message': 'A tag \'{}\' is unknown'.format(tag.name)}

        new_post = PostModel(**data)
        try:
            new_post.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return new_post.get_json(), 201


class Post(Resource):
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

    parser.add_argument('tags',
                        type=list,
                        required=True,
                        help='This field cannot be blank.')

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

    def put(self, _id):
        data = Post.parser.parse_args()
        post = PostModel.find_by_id(_id)
        if not post:
            post = PostRegister.post()
        else:
            post.title = data['title']
            post.body = data['body']
            post.user_id = data['user_id']
            post.is_published = data['is_published']
        post.save_to_db()
        return item.json(), 200


class PostList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help='This field cannot be blank.')

    def get(self):
        return {'posts': [post.get_json() for post in PostModel.query.all()]}


class PostStatistics(Resource):
    def get(self):
        return {'posts': PostModel.query.count(),
                'published posts': PostModel.query.filter(PostModel.is_published).count(),
                'drafts': PostModel.query.filter(not PostModel.is_published).count()}
