from flask import Flask

from flask_restful import Api

from config import Configuration

from resources.post import Post
from resources.post import PostList
from resources.post import PostRegister
from resources.post import PostStatistics
from resources.tag import TagList
from resources.tag import TagRegister

app = Flask(__name__)
app.config.from_object(Configuration)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Post, '/post/<int:_id>')
api.add_resource(PostRegister, '/post')
api.add_resource(PostList, '/posts')
api.add_resource(PostStatistics, '/statistics')
api.add_resource(TagRegister, '/tag/<string:name>')
api.add_resource(TagList, '/tags')


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=1234, debug=True)
