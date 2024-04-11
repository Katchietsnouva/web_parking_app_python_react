# app/models/user_model.py
class UserModel:
    def __init__(self, user_id, customer_no, username, password, phone, email, carmanufacturer, carmodel, car_plate, role='user'):
        # ... other fields ...
        self.user_id = user_id
        self.customer_number = customer_no
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.carmanufacturer = carmanufacturer
        self.carmodel = carmodel
        self.car_plate = car_plate
        self.role = role



# # app/models/user_model.py
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     name = db.Column(db.String(80), nullable=False)
#     phone = db.Column(db.String(15), nullable=False)
#     car_plate = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>'


