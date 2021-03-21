from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
        
class ROOM(db.Model):
    room_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    room_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ROOM(room_id = {self.room_id}, room_type = {self.room_type})"
    
class CUSTOMER(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    customer_name = db.Column(db.String(100), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.String(50), nullable=False)
    check_out = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float)
    room_id = db.Column(db.Integer, db.ForeignKey('ROOM.room_id'), nullable=False)
    booking_type = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    stay_days_number = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"""CUSTOMER(customer_id = {self.customer_id}, 
    customer_name = {self.customer_name}, 
    number_of_people = {self.number_of_people}, 
    check_in = {self.check_in}, 
    check_out = {self.check_out}, 
    price_per_night = {self.price_per_night}, 
    room_id = {self.room_id}, 
    booking_type = {self.booking_type}, 
    comment = {self.comment}, 
    stay_days_number = {self.stay_days_number},
    deleted = {self.deleted})"""