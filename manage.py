from flask_script import Manager ,Server# class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import Quotes

app = create_app('production')


manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,Quotes = Quotes)



if __name__ == '__main__':
    manager.run()