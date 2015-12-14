#!/usr/bin/env python

import os

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean
from neogameserver import create_app
from neogameserver.models import db, User

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('neogameserver_ENV', 'dev')
app = create_app('neogameserver.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, User=User)


if __name__ == "__main__":
    manager.run()
