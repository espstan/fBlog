from flask import request
from flask import jsonify

from sqlalchemy.exc import SQLAlchemyError

from app import app
from app import db

from models import Post

from config import Configuration


#POST - создать новый пост=создать черновик
@app.route('/posts', methods=['POST'])
def create_post():
    request_data = request.get_json()

    if request_data['title']:
        if len(request_data['title']) <= Configuration.MAX_TITLE_SIZE:
            try:
                post = Post(title=request_data['title'], body=request_data['body'])
                db.session.add(post)
                db.session.commit()
            except SQLAlchemyError as e:
                err = str(e.__class__.__name__)
                return jsonify({'SQLAlchemy error:': err})
            return jsonify({'title': post.title,
                            'body': post.body
                            })
        else:
            return jsonify({'message': 'len(title) > {}'.format(Configuration.MAX_TITLE_SIZE)})
    return jsonify({'message': 'your post has no title'})
