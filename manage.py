import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..')

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main.model import user,user_credentials,user_session,subscribers,services,brands,brand_subscribers_relation,brand_user_relation

from app.main import create_app, db
from flask_cors import CORS

app = create_app('dev')
CORS(app, resources={r"/": {"origins": "*"}})
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    db.create_all()
    app.run(port=80)


if __name__ == '__main__':
    manager.run()
