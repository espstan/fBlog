from flask import Flask

from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy

from config import Configuration


app = Flask(__name__)

app.config.from_object(Configuration)
db = SQLAlchemy(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from models import Post
