from flask_restful import fields


resource_fields_ROOM = {
    'room_id': fields.Integer(default=None),
    'room_type': fields.Integer(default=None),
    'message': fields.String(default=None),
    'room': fields.String(default=None)
}

resource_fields_CUSTOMER = {
    'customer_id': fields.Integer(default=None),
    'customer_name': fields.String(default=None),
    'number_of_people': fields.Integer(default=None),
    'check_in': fields.String(default=None),
    'check_out': fields.String(default=None),
    'price_per_night': fields.Float(default=None),
    'room_id': fields.Integer(default=None),
    'booking_type': fields.Integer(default=None),
    'comment': fields.String(default=None),
    'stay_days_number': fields.Integer(default=None),
    'message': fields.String(default=None),
    'customer': fields.String()
}

class ResourceFields():
    def __init__(self) -> None:
        self.room = resource_fields_ROOM
        self.customer = resource_fields_CUSTOMER

resource_fields = ResourceFields()