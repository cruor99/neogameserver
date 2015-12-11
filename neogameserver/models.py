from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    role = db.Column(db.String())

    def __init__(self, username, password, email, role):
        self.username = username
        self.set_password(password)
        self.email = email
        self.role = role

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

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
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Subscription(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user = db.relationship("User", foreign_keys="[Subscription.userid]")
    startdate = db.Column(db.DateTime(), default=datetime.datetime.now())
    enddate = db.Column(db.DateTime())
    productid = db.Column(db.Integer(), db.ForeignKey("order_product.id"))
    product = db.relationship("OrderProduct", foreign_keys="[Subscription.productid]")

    def __init__(self, userid=None, enddate=None, productid=None):
        self.userid = userid
        self.enddate = enddate
        self.productid = productid


class OrderProduct(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    mcproduct = db.Column(db.Integer(), db.ForeignKey("minecraft_product.id"))
    mcport = db.Column(db.Integer(), db.ForeignKey("port.id"))
    ventproduct = db.Column(db.Integer(), db.ForeignKey("ventrilo_product.id"))
    ventport = db.Column(db.Integer(), db.ForeignKey("port.id"))
    minecraft_product = db.relationship("MinecraftProduct",
                                        foreign_keys="[OrderProduct.mcproduct]")
    ventrilo_product = db.relationship("VentriloProduct",
                                       foreign_keys="[OrderProduct.ventproduct]")
    ventrilo_port = db.relationship("Port", foreign_keys="[OrderProduct.ventport]")
    minecraft_port = db.relationship("Port", foreign_keys="[OrderProduct.mcport]")



    def __init__(self, mcproduct=None, ventproduct=None):
        self.mcproduct = mcproduct
        self.ventproduct = ventproduct


    def __repr__(self):
        return "<Order: MC: {}, Vent:{}".format(self.mcproduct, self.ventproduct)


class HostServer(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    servername = db.Column(db.String(), unique = True)
    serverip = db.Column(db.String(), unique = True)

    def __init__(self, servername=None, serverip=None):
        self.servername = servername
        self.serverip = serverip

    def __repr__(self):
        return "<HostServer: {}".format(self.servername)


class Port(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    portnumber = db.Column(db.Integer)
    taken = db.Column(db.String())
    hostserver = db.Column(db.Integer(), db.ForeignKey("host_server.id"))
    host_server = db.relationship("HostServer", foreign_keys = "[Port.hostserver]")

    def __init__(self, portnumber=None, taken=None, hostserver=None):
        self.portnumber = portnumber
        self.taken = taken
        self.hostserver = hostserver

    def __repr__(self):
        return "<Portnumber: {}".format(self.portnumber)





class MinecraftProduct(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    dedicated_ram = db.Column(db.Integer)
    # price in USD
    price = db.Column(db.Integer)
    description = db.Column(db.String())

    def __repr__(self):
        return "<Description: %r>" % self.description


class VentriloProduct(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    slots = db.Column(db.Integer)
    # price in USD
    price_per_slot = db.column(db.Integer)
    description = db.Column(db.String())

    def __repr__(self):
        return "<Description %r>" %self.description
