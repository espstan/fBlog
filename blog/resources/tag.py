from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.post import PostModel

from models.tag import TagModel


class TagRegister(Resource):




    def delete(self, name):

        pass


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