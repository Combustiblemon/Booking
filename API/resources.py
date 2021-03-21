from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.BaseModels import db, ROOM, CUSTOMER
import datetime

#region ROOM logic

ROOM_get_args = reqparse.RequestParser()
ROOM_get_args.add_argument("room_id", type=int, help="id of the room is required")
ROOM_get_args.add_argument("room_type", type=int, help="Type of the room is required")

ROOM_put_args = reqparse.RequestParser()
ROOM_put_args.add_argument("room_type", type=int, help="Type of the room is required", required=True)

ROOM_update_args = reqparse.RequestParser()
ROOM_update_args.add_argument("room_id", type=str, help="id of the room is required", required=True)
ROOM_update_args.add_argument("room_type", type=int, help="type of the room is required", required=True)

ROOM_delete_args = reqparse.RequestParser()
ROOM_delete_args.add_argument("room_id", type=int, help="id of the room is required", required=True)

resource_fields_ROOM = {
    'room_id': fields.Integer,
    'room_type': fields.Integer,
}

class Rooms(Resource):
    @marshal_with(resource_fields_ROOM)
    def get(self):
        args = ROOM_get_args.parse_args()
        if args['room_id']:
            result = ROOM.query.filter_by(room_id=args['room_id']).first()
        elif args['room_type']:
            result = ROOM.query.filter_by(room_id=args['room_type'])
            
        if not result:
            abort(404, message="Could not find room with that id")
        return result

    @marshal_with(resource_fields_ROOM)
    def put(self):
        args = ROOM_put_args.parse_args()
        result = ROOM.query.filter_by(room_id=args['room_id']).first()
        if result:
            abort(409, message="Room id taken...")

        room = ROOM(room_id=None, room_type=args['room_type'])
        db.session.add(room)
        db.session.commit()
        return room, 201

    @marshal_with(resource_fields_ROOM)
    def patch(self):
        args = ROOM_update_args.parse_args()
        result = ROOM.query.filter_by(room_id=args['room_id']).first()
        if not result:
            abort(404, message=f"Room with room_id={args['room_id']} doesn't exist, cannot update")
        
        result.room_type = args['room_type']

        db.session.commit()

        return result

    @marshal_with(resource_fields_ROOM)
    def delete(self):
        args = ROOM_delete_args.parse_args()
        result = ROOM.query.filter_by(room_id=args['room_id']).first()
        if not result:
            abort(404, message="Room id not found...")

        temp = result
        db.session.delete(result)
        db.session.commit()
        return temp, 204
    
#endregion
    
#region CUSTOMER logic

#region args logic
CUSTOMER_get_args = reqparse.RequestParser()
CUSTOMER_get_args.add_argument("customer_id", type=int, help="id of the room is required")
CUSTOMER_get_args.add_argument("customer_name", type=str, help="Type of the room is required")
CUSTOMER_get_args.add_argument("number_of_people", type=int, help="Type of the room is required")
CUSTOMER_get_args.add_argument("check_in", type=str, help="Type of the room is required")
CUSTOMER_get_args.add_argument("check_out", type=str, help="Type of the room is required")
CUSTOMER_get_args.add_argument("price_per_night", type=float, help="Type of the room is required")
CUSTOMER_get_args.add_argument("room_id", type=int, help="Type of the room is required")
CUSTOMER_get_args.add_argument("booking_type", type=int, help="Type of the room is required")
CUSTOMER_get_args.add_argument("stay_days_number", type=int, help="Type of the room is required")
CUSTOMER_get_args.add_argument("deleted", type=bool, help="if the customer is deleted")

CUSTOMER_put_args = reqparse.RequestParser()
CUSTOMER_put_args.add_argument("customer_name", type=str, help="customer_name is required", required=True)
CUSTOMER_put_args.add_argument("number_of_people", type=int, help="number_of_people is required", required=True)
CUSTOMER_put_args.add_argument("check_in", type=str, help="check_in is required", required=True)
CUSTOMER_put_args.add_argument("check_out", type=str, help="check_out is required", required=True)
CUSTOMER_put_args.add_argument("price_per_night", type=float, help="price_per_nightm is required", required=True)
CUSTOMER_put_args.add_argument("room_id", type=int, help="room_id is required", required=True)
CUSTOMER_put_args.add_argument("booking_type", type=int, help="booking_type is required", required=True)
CUSTOMER_put_args.add_argument("comment", type=str, help="comment is required")
CUSTOMER_put_args.add_argument("stay_days_number", type=int, help="stay_days_number is required", required=True)

CUSTOMER_update_args = reqparse.RequestParser()
CUSTOMER_update_args.add_argument("customer_id", type=int, help="id of the room is required", required=True)
CUSTOMER_update_args.add_argument("customer_name", type=str, help="Type of the room is required")
CUSTOMER_update_args.add_argument("number_of_people", type=int, help="Type of the room is required")
CUSTOMER_update_args.add_argument("check_in", type=str, help="Type of the room is required")
CUSTOMER_update_args.add_argument("check_out", type=str, help="Type of the room is required")
CUSTOMER_update_args.add_argument("price_per_night", type=float, help="Type of the room is required")
CUSTOMER_update_args.add_argument("room_id", type=int, help="Type of the room is required")
CUSTOMER_update_args.add_argument("booking_type", type=int, help="Type of the room is required")
CUSTOMER_update_args.add_argument("comment", type=str, help="Type of the room is required")
CUSTOMER_update_args.add_argument("stay_days_number", type=int, help="Type of the room is required")

CUSTOMER_delete_args = reqparse.RequestParser()
CUSTOMER_delete_args.add_argument("customer_id", type=int, help="id of the customer is required", required=True)

#endregion

resource_fields_CUSTOMER = {
    'customer_id': fields.Integer,
    'customer_name': fields.String(100),
    'number_of_people': fields.Integer,
    'check_in': fields.String,
    'check_out': fields.String,
    'price_per_night': fields.Float,
    'room_id': fields.Integer,
    'booking_type': fields.Integer,
    'comment': fields.String(500),
    'stay_days_number': fields.Integer,
    'deleted': fields.Boolean,
}

class Customers(Resource):
    @marshal_with(resource_fields_CUSTOMER)
    def get(self):
        args = CUSTOMER_get_args.parse_args()
        
        #build the query object dynamically
        query = CUSTOMER.query.filter_by()
        if args['customer_id']:
            query = query.filter_by(customer_id=args['customer_id'])
        if args['customer_name']:
            query = query.filter_by(customer_name=args['customer_name'])
        if args['number_of_people']:
            query = query.filter_by(number_of_people=args['number_of_people'])
        if args['check_in']:
            query = query.filter_by(check_in=args['check_in'])
        if args['check_out']:
            query = query.filter_by(check_out=args['check_out'])
        if args['price_per_night']:
            query = query.filter_by(price_per_night=args['price_per_night'])
        if args['room_id']:
            query = query.filter_by(room_id=args['room_id'])
        if args['booking_type']:
            query = query.filter_by(booking_type=args['booking_type'])  
        if args['stay_days_number']:
            query = query.filter_by(stay_days_number=args['stay_days_number'])
        if args['deleted']:
            query = query.filter_by(deleted=args['deleted'])

        #then finally execute it

        results = query.all()
            
        if not results:
            abort(404, message="Could not find room with that id")
        return results

    @marshal_with(resource_fields_CUSTOMER)
    def put(self):
        args = CUSTOMER_put_args.parse_args()
        room = ROOM.query.filter_by(room_id=args['room_id']).first()
        
        if not room:
            abort(404, message="Room doesn't exist, please create the room first")
        
        result = CUSTOMER.query.filter_by(customer_name=args['customer_name'],
                                          number_of_people=args['number_of_people'],
                                          check_in=args['check_in'],
                                          check_out=args['check_out'],
                                          room_id=args['room_id'],
                                          booking_type=args['booking_type'],).first()
        if result:
            abort(409, message="Customer already exists...")

        if not args['comment']:
            args['comment'] = ''
        
        customer = CUSTOMER(customer_id=None, 
                            customer_name=args['customer_name'], 
                            number_of_people=args['number_of_people'], 
                            check_in=args['check_in'], 
                            check_out=args['check_out'], 
                            price_per_night=args['price_per_night'],
                            room_id=args['room_id'],
                            booking_type=args['booking_type'],
                            comment=args['comment'],
                            stay_days_number=args['stay_days_number'],
                            deleted=False)
        
        db.session.add(customer)
        db.session.commit()
        return customer, 201

    @marshal_with(resource_fields_CUSTOMER)
    def patch(self):
        args = CUSTOMER_update_args.parse_args()
        room = ROOM.query.filter_by(room_id=args['room_id']).first()
        
        if not room:
            abort(404, message="Room doesn't exist, please create the room first")
        
        result = CUSTOMER.query.filter_by(customer_id=args['customer_id']).first()
        if not result:
            abort(404, message=f"Customer with customer_id={args['customer_id']} doesn't exist, cannot update")
        
        if args['customer_name']:
            result.customer_name = args['customer_name']
        if args['number_of_people']:
            result.number_of_people = args['number_of_people']
        if args['check_in']:
            result.check_in = args['check_in']
        if args['check_out']:
            result.check_out = args['check_out']
        if args['price_per_night']:
            result.price_per_night = args['price_per_night']
        if args['room_id']:
            result.room_id = args['room_id']
        if args['booking_type']:
            result.booking_type = args['booking_type']
        if args['comment']:
            result.comment = args['comment']
        if args['stay_days_number']:
            result.stay_days_number = args['stay_days_number']

        db.session.commit()

        return result

    @marshal_with(resource_fields_CUSTOMER)
    def delete(self):
        args = CUSTOMER_delete_args.parse_args()
        result = CUSTOMER.query.filter_by(customer_id=args['customer_id']).first()
        if not result:
            abort(404, message="Customer id not found...")

        result.deleted = True
        
        db.session.commit()
        
        return result, 204
    
#endregion