import json
import time
from typing import Iterable
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from marshmallow import fields, ValidationError
import marshmallow


db = SQLAlchemy()
ma = Marshmallow()

#region OAUTH models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        if password == self.password:
            return True
        else:
            return False


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()


#endregion

#region API models

class ROOM(db.Model):
    room_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    room_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"(room_id = {self.room_id}, room_type = {self.room_type})"
    
    def __dir__() -> Iterable[str]:
        return ['room_id', 'room_type']


class RoomSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ROOM
        include_fk = True
        manu = True
    
    room_id = fields.Integer()
    room_type = fields.Integer()
    filters = fields.List(
        fields.Tuple(
            (
                fields.Str(), 
                fields.Field(), 
                fields.Str()
            )
        )
    )

    
class CUSTOMER(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    customer_name = db.Column(db.String(100), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.String(50), nullable=False)
    check_out = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float, default=0.0)
    room_id = db.Column(db.Integer, db.ForeignKey('ROOM.room_id'), nullable=False)
    booking_type = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), default='')
    stay_days_number = db.Column(db.Integer, nullable=False)
    
    @property
    def serialize(self):
        return {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'number_of_people': self.number_of_people,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'price_per_night': self.price_per_night,
            'room_id': self.room_id,
            'booking_type': self.booking_type,
            'comment': self.comment,
            'stay_days_number': self.stay_days_number
        }
        
    
    def __dir__() -> Iterable[str]:
        return ['customer_id',
                'customer_name',
                'number_of_people',
                'check_in',
                'check_out',
                'price_per_night',
                'room_id',
                'booking_type',
                'comment',
                'stay_days_number']

class StrListField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, list):
            return value
        else:
            raise ValidationError('Field should be either string or list')

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CUSTOMER        

    customer_id = fields.Integer()
    customer_name = fields.Str()
    number_of_people = fields.Integer()
    check_in = fields.String()
    check_out = fields.String()
    price_per_night = fields.Float()
    room_id = fields.Integer()
    booking_type = fields.Integer()
    comment = fields.String()
    stay_days_number = fields.Integer()
    filters = fields.List(
        fields.Tuple(
            (
                StrListField(), 
                fields.Field(), 
                fields.Str()
            )
        )
    )

#endregion