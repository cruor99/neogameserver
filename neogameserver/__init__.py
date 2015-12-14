#! ../env/bin/python

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.admin import Admin
from flask.ext.admin.contrib.mongoengine import ModelView

from neogameserver import assets
from neogameserver.models import db, User, MinecraftProduct, VentriloProduct
from neogameserver.models import Hostserver, Port
from neogameserver.controllers.main import main

from neogameserver.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)


def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. neogameserver.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize MongoEngine
    db.init_app(app)

    login_manager.init_app(app)

    # Flask Admin stuff
    admin = Admin(app, "Neogameserver: Mongoengine")

    admin.add_view(ModelView(User))
    admin.add_view(ModelView(MinecraftProduct))
    admin.add_view(ModelView(VentriloProduct))
    admin.add_view(ModelView(Hostserver))
    admin.add_view(ModelView(Port))


    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)

    return app
