from data import db_session
from data.admins import Admin

def push_data():
    session = db_session.create_session()
    user = Admin()
    user.name = 'admin'
    user.set_password('admin')
    session.add(user)
    session.commit()