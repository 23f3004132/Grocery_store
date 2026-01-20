from app import app
from models import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

with app.app_context():
    db.drop_all()
    db.create_all()
    datastore: SQLAlchemyUserDatastore = app.datastore

    admin_role = datastore.find_or_create_role(name='admin', description='super_user')
    manager_role = datastore.find_or_create_role(name='manager', description='handels and manages store')
    customer_role = datastore.find_or_create_role(name='customer', description='buy items from store')

    if not datastore.find_user(email='admin@study'):
        datastore.create_user(
            email = 'admin@study',
            name = 'Admin_1',
            password= hash_password("pass"),
        )
    if not datastore.find_user(email='manager@study'):
        datastore.create_user(
            email = 'manager@study',
            name = 'Manager_1',
            password= hash_password("pass")
        )
    if not datastore.find_user(email='customer@study'):
        datastore.create_user(
            email = 'customer@study',
            name = 'Customer_1',
            password= hash_password("pass")
        )
    try:
        db.session.commit()
    except:
        db.session.rollback()


    Admin_1 = datastore.find_user(email='admin@study')
    Manager_1 = datastore.find_user(email='manager@study')
    Customer_1 = datastore.find_user(email='customer@study')

    admin_role = datastore.find_role('admin')
    manager_role = datastore.find_role('manager')   
    customer_role = datastore.find_role('customer')

    datastore.add_role_to_user(Admin_1, admin_role)
    datastore.add_role_to_user(Manager_1, manager_role)     
    datastore.add_role_to_user(Customer_1, customer_role)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()