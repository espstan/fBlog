import json

import urllib.request

from sqlalchemy.exc import SQLAlchemyError

from db import db

from models.post import PostModel as PM

from models.comment import CommentModel as CM

url_posts = "https://jsonplaceholder.typicode.com/posts"
url_comments = "https://jsonplaceholder.typicode.com/comments"


class LoadData():
    @staticmethod
    def load_posts():
        with urllib.request.urlopen(url_posts) as url:
            data = json.loads(url.read().decode())
            for post in data:
                try:
                    db.session.add(PM(title=post['title'],
                                      body=post['body'],
                                      user_id=post['userId'],
                                      is_published=True))
                    db.session.commit()
                except SQLAlchemyError as e:
                    err = str(e.__class__.__name__)
                    return {'message': '{}'.format(err)}, 500
            return "Success"

    @staticmethod
    def load_comments():
        with urllib.request.urlopen(url_comments) as url:
            data = json.loads(url.read().decode())
            for comment in data:
                try:
                    db.session.add(CM(name=comment['name'],
                                      body=comment['body'],
                                      email=comment['email'],
                                      post_id=comment['postId']))
                    db.session.commit()
                except SQLAlchemyError as e:
                    err = str(e.__class__.__name__)
                    return {'message': '{}'.format(err)}, 500
            return "Success"
