from flask_restful import Resource
from flask_restful import reqparse

from sqlalchemy.exc import SQLAlchemyError

from config import Configuration

from models.post import PostModel

from models.tag import TagModel

from models.category import CategoryModel as CM

from models.comment import CommentModel


def get_tags(tag_names):
    tags = []
    for name in tag_names:
        tag = TagModel.find_by_name(name)
        if tag:
            tags.append(tag)
        else:
            return {'message': 'There is no such tag: \'{}\''.format(name)}
    return tags


def get_comments(comments_id):
    comments = []
    for comment_id in comments_id:
        comment = CommentModel.find_by_name(comment_id)
        if comment:
            comments.append(comment)
        else:
            return {'message': 'There is no such comment: \'{}\''.format(_id)}
    return comments


def get_item_tags(tags, post):
    for tag in set(tags):
        if TagModel.query.filter(TagModel.name == tag.name).first():
            post.tags.append(tag)
        else:
            return {'message': 'There is no such tag: \'{}\''.format(tag.name)}
    return post


def get_item_comments(comments, post):
    for comment in set(comments):
        if CommentModel.query.filter(CommentModel.id == comment.id).first():
            post.comments.append(comment)
        else:
            return {'message': 'There is no such comment: \'{}\''.format(comment.id)}
    return post


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
                        type=str,
                        action='append',
                        required=False)

    parser.add_argument('category_id',
                        type=int,
                        required=False)

    parser.add_argument('comments',
                        type=int,
                        action='append',
                        required=False)

    def post(self):
        data = PostRegister.parser.parse_args()
        tag_names = data['tags']
        if tag_names:
            tags = get_tags(tag_names)
        else:
            tags = []

        if len(data['title']) > Configuration.MAX_POST_TITLE_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_POST_TITLE_SIZE)}

        category = data['category_id']
        if category:
            if not CM.query.filter(CM.id == category).first():
                return {'message': 'There is no such category: \'{}\''.format(category)}

        comments_id = data['comments']
        if comments_id:
            comments = get_comments(comments_id)
        else:
            comments = []

        del data['tags']
        del data['category_id']
        del data['comments']

        new_post = PostModel(**data)

        if tags:
            new_post = get_item_tags(tags, new_post)
        if comments:
            new_post = get_item_comments(comments, new_post)

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
                        type=str,
                        action='append',
                        required=False)

    parser.add_argument('category_id',
                        type=int,
                        required=False)
    parser.add_argument('comments',
                        type=int,
                        action='append',
                        required=False)

    def put(self, _id):
        data = Post.parser.parse_args()

        if len(data['title']) > Configuration.MAX_POST_TITLE_SIZE:
            return {'message': 'A title\'s length is more than {}'.format(Configuration.MAX_POST_TITLE_SIZE)}
        category = data['category_id']
        if category:
            if not CM.query.filter(CM.id == category).first():
                return {'message': 'There is no such category: \'{}\''.format(category)}

        tag_names = data['tags']
        if tag_names:
            tags = get_tags(tag_names)
        else:
            tags = []

        comments_id = data['comments']
        if comments_id:
            comments = get_comments(comments_id)
        else:
            comments = []

        del data['tags']
        del data['category_id']
        del data['comments']

        post = PostModel.find_by_id(_id)
        if not post:
            post = PostModel(**data)
            if tags:
                post = get_item_tags(tags, post)
            if comments:
                post = get_item_comments(comments, post)
        else:
            post.title = data['title']
            post.body = data['body']
            post.user_id = data['user_id']
            post.is_published = data['is_published']
            post.category_id = category
            post.tags = []
            post.comments = []
            if tags:
                post = get_item_tags(tags, post)
            if comments:
                post = get_item_comments(comments, post)

        try:
            post.save_to_db()
        except SQLAlchemyError as e:
            err = str(e.__class__.__name__)
            return {'message': '{}'.format(err)}, 500
        return post.get_json(), 201


class PostList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('deleted_posts',
                        type=int,
                        action='append',
                        required=True,
                        help='This field cannot be blank.')

    def get(self):
        return {'posts': [post.get_json() for post in PostModel.query.all()]}

    def delete(self):
        data = PostList.parser.parse_args()
        deleted_posts = []
        messages = []
        for post_id in data['deleted_posts']:
            if str(post_id).isdigit():
                post = PostModel.find_by_id(post_id)
                if post:
                    try:
                        post.delete_from_db()
                    except SQLAlchemyError as e:
                        err = str(e.__class__.__name__)
                        return {'message': '{}'.format(err)}, 500
                    deleted_posts.append(post_id)
                else:
                    messages.append({post_id: 'Post with id={} was not found'.format(post_id)})
            else:
                messages.append({post_id: 'id must be a number'})
        if not messages:
            messages.append({'status': "done"})
        return {'deleted_posts': deleted_posts,
                'messages': messages}


class PostStatistics(Resource):
    def get(self):
        return {'posts': PostModel.query.count(),
                'published posts': PostModel.query.filter(PostModel.is_published).count(),
                'drafts': PostModel.query.filter(PostModel.is_published == False).count()}
