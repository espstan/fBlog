from flask_migrate import Migrate
from flask_migrate import MigrateCommand

# from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy

# from app import app

db = SQLAlchemy()


# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
