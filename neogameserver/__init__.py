#! ../env/bin/python

from flask import Flask
from flask_admin import Admin
from webassets.loaders import PythonLoader as PythonAssetsLoader

from neogameserver import assets
from neogameserver.models import db, User, Subscription, MinecraftProduct, VentriloProduct
from neogameserver.models import OrderProduct, HostServer, Port
from neogameserver.controllers.main import main
from neogameserver.controllers.adminviews import adminviews, NeoModelView

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

    admin = Admin(app, name="neogameserver", template_mode="bootstrap3")
    admin.add_view(NeoModelView(User, db.session))
    admin.add_view(NeoModelView(Subscription, db.session))
    admin.add_view(NeoModelView(MinecraftProduct, db.session))
    admin.add_view(NeoModelView(VentriloProduct, db.session))
    admin.add_view(NeoModelView(OrderProduct, db.session))
    admin.add_view(NeoModelView(HostServer, db.session))
    admin.add_view(NeoModelView(Port, db.session))

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)
    app.register_blueprint(adminviews)

    return app
