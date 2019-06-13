from flask import Flask

from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from flask_restful import Api

from flask_script import Manager

from config import Configuration

from resources.post import PostList
from resources.post import PostRegister
from resources.post import PostStatistics

app = Flask(__name__)
app.config.from_object(Configuration)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(PostRegister, '/post')
api.add_resource(PostList, '/posts')
api.add_resource(PostStatistics, '/statistics')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    app.run(port=1234, debug=True)
