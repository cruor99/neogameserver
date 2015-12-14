from flask.ext.mongoengine import MongoEngine
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

db = MongoEngine()



class Hostserver(db.Document):

    servername = db.StringField()
    serverip = db.StringField()

    def __unicode__(self):
        return self.servername


class Port(db.Document):

    portnumber = db.StringField()
    taken = db.StringField()
    hostserver = db.ReferenceField(Hostserver)

    def __unicode__(self):
        return "Portnumber: {}, Taken: {}".format(self.portnumber, self.taken)


class Product(db.Document):

    startdate = db.DateTimeField(default=datetime.datetime.now())
    enddate = db.DateTimeField()
    productname = db.StringField()
    baseprice = db.IntField()
    port = db.ReferenceField(Port)
    description = db.StringField()

    meta = {
        "allow_inheritance": True
    }

    def __unicode__(self):
        return self.productname



class User(db.Document, UserMixin):
    # id = db.Column(db.Integer(), primary_key=True)
    # username = db.Column(db.String(), unique=True)
    # password = db.Column(db.String())
    # email = db.Column(db.String(), unique=True)
    # role = db.Column(db.String())

    # _id = ObjectId("23403480")
    username = db.StringField(required = True, unique=True, verbose_name="Username",
                              help_text="Username is required")
    password = db.StringField(required = True, verbose_name = "Password Hash",
                              help_text="Password Hash should be provided")
    email = db.StringField(required = True, unique=True, verbose_name="Email",
                           help_text="Email is required")
    role = db.StringField(Required = True, verbose_name="Role", help_text="Role is required")
    products = db.ListField(db.ReferenceField(Product))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @classmethod
    def check_password(self, password, value):
        return check_password_hash(password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.username

    def __unicode__(self):
        return self.username


# Different products inherit from Product baseclass to be listed in the subcription


class MinecraftProduct(Product):

    dedicated_ram = db.IntField()


class VentriloProduct(Product):

    slots = db.IntField()
