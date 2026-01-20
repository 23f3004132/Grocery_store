from extentions import db
from datetime import datetime
from flask_security.core import UserMixin, RoleMixin

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    roles = db.relationship('Role', secondary='user_roles', backref='bearers', lazy=True)

    requests = db.relationship('Request', backref='user', lazy=True)
    sales = db.relationship('Sale', backref='customer', lazy=True)

class Role(BaseModel, RoleMixin):
    __tablename__ = 'role'

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class UserRoles(BaseModel):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Manager(BaseModel):
    __tablename__ = 'managers'

    salary = db.Column(db.Float, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Customer(BaseModel):
    __tablename__ = 'customer'

    loyalty_points = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Request(BaseModel):
    __tablename__ = 'requests'

    data = db.Column(db.JSON, nullable=True)
    status = db.Column(db.Enum('approved', 'rejected', 'created'), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Section(BaseModel):
    __tablename__ = 'sections'

    name = db.Column(db.String(100), nullable=False)

    products = db.relationship('Product', backref='section', lazy=True)

class Product(BaseModel):
    __tablename__ = 'products'

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    expiry_date = db.Column(db.DateTime(timezone=True), nullable=True)
    mfd = db.Column(db.DateTime(timezone=True), nullable=True)
    unit_of_sale = db.Column(db.Enum("kg", "litre", "unit"), nullable=True)

    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

    sale_items = db.relationship('SaleItem', backref='product', lazy=True)

class Sale(BaseModel):
    __tablename__ = 'sales'

    total_amount = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    sale_items = db.relationship('SaleItem', backref='sale', lazy=True)

class SaleItem(BaseModel):
    __tablename__ = 'sale_items'

    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Float, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
