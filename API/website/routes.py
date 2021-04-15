import time
from datetime import date
import re
from flask import Blueprint, json, request, session, url_for
from flask import render_template, redirect, jsonify
from flask.wrappers import Response
from flask_restful import marshal_with, abort
import marshmallow
from requests.api import delete
from werkzeug.security import gen_salt
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from .models import RoomSchema, db, User, OAuth2Client, ROOM, CUSTOMER, CustomerSchema
from .oauth2 import authorization, require_oauth
from .resources import resource_fields
from .utilities import constructDBQuery, getReturnObject


bp = Blueprint(__name__, 'home')

#region OAUTH logic

def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template('error.html', message='Username not valid. Please contact an administrator if you are lacking an account.')
        if not user.check_password(password):
            return render_template('error.html', message='Password not valid.')
        
        session['id'] = user.id
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/')
    user = current_user()
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('home.html', user=user, clients=clients)


@bp.route('/logout')
def logout():
    del session['id']
    return redirect('/')


@bp.route('/create_client', methods=('GET', 'POST'))
def create_client():
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()
    return redirect('/')


@bp.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    # if user log status is not true (Auth server), then to log it in
    if not user:
        return redirect(url_for('website.routes.home', next=request.url))
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')

#endregion

#region API logic

@bp.after_request
def remove_none_fields(resp: Response, fields=None):
    """
    removes all None fields
    """
    
    if 'application/json' not in resp.content_type:
        return resp

    def dict_remove(d, fields):
        if fields:
            for field in fields:
                if d[field] is None:
                    d.pop(field)
        else:
            for k, v in tuple(d.items()):
                if isinstance(v, dict):
                    dict_remove(v, fields) 
                elif isinstance(v, list):
                    for obj in v:
                        dict_remove(obj, fields) 
                elif v is None:
                    d.pop(k)

    data = json.loads(resp.get_data())
    if isinstance(data, list):
        for obj in data:
            dict_remove(obj, fields)
    else:
        dict_remove(data, fields)

    resp.set_data(json.dumps(data, indent=1))
    resp.content_length = resp.calculate_content_length()
    return resp

def getJSONFromRequest(request: request) -> str:
    args = request.get_json(silent=True)
    if not args:
        abort(400, message={'message': "Bad request. Data needs to be sent in JSON format."})
    
    return args
    
@bp.route('/api/me')
@require_oauth('api')
def api_me():
    print(current_token)
    user = current_token.user
    return jsonify(id=user.id, username=user.username)


@bp.route('/echo', methods=['POST', 'GET', 'PUT', 'DELETE'])
#@marshal_with(resource_fields.room)
def echo():
    # args = request_arguments.room.get.parse_args()
    #print(data, request.get_data(), sep='\n')
    args = request.get_json(silent=True)
    
    if args:
        return args
    return {"nope0": "nada"}

#region ROOM logic

@bp.route('/api/rooms', methods=['PATCH', 'GET', 'PUT', 'DELETE'])
@require_oauth('api')
@marshal_with(resource_fields.room, envelope='rooms')
def api_rooms():
    schemaRoom = RoomSchema()
    JSONdata = getJSONFromRequest(request)
    if request.method == 'PUT':        
        try:
            args = schemaRoom.loads(JSONdata)
            
            result = ROOM.query.filter_by(room_id=args['room_id']).first()
            
            if result:
                return getReturnObject(400, message='Room ID already exists')

            room = ROOM(room_id=args['room_id'], room_type=args['room_type'])
            db.session.add(room)
            db.session.commit()
            return getReturnObject(200, message='Put operation completed successfully', room=room)
        
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
        
    elif request.method == 'PATCH':
        try:
            args = schemaRoom.loads(JSONdata)
            result = constructDBQuery(ROOM, args['filters']).all()
            if len(result) == 0:
                return getReturnObject(404, message="Room doesn't exist, cannot update")
            
            for item in result:
                item.room_type = args['room_type']
            
            db.session.commit()

            return getReturnObject(200, message='PATCH operation successful.', room=result)
        
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
        
    elif request.method == 'GET':
        try: 
            args = schemaRoom.loads(JSONdata)
            result = constructDBQuery(ROOM, args['filters']).all()
            
            return getReturnObject(200, room=result) 
        
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
        
    elif request.method == 'DELETE':        
        try:
            args = schemaRoom.loads(JSONdata)
            result = constructDBQuery(ROOM, args['filters']).all()
            if len(result) == 0:
                return getReturnObject(404, message=f'Room not found.\n filter: {args["filters"]}')
            
            for item in result:
                db.session.delete(item)
            db.session.commit()
            return getReturnObject(204, message='DELETE operation successful')
        
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
        
#endregion

#region CUSTOMER logic

@bp.route('api/customers', methods=['PATCH', 'GET', 'PUT', 'DELETE'])
@require_oauth('api')
@marshal_with(resource_fields.customer, envelope='customers')
def api_customers():
    schemaCustomer = CustomerSchema()
    JSONdata = getJSONFromRequest(request)
    if request.method == 'PUT':
        try:
            args = schemaCustomer.loads(JSONdata)
            room = ROOM.query.filter_by(room_id=args['room_id']).first()
            
            if not room:
                return getReturnObject(404, message='Room does not exist.')
            
            result = CUSTOMER.query.filter_by(customer_name=args['customer_name'],
                                              number_of_people=args['number_of_people'],
                                              check_in=args['check_in'],
                                              check_out=args['check_out'],
                                              room_id=args['room_id'],
                                              booking_type=args['booking_type'],
                                              ).first()
            if result:
                return getReturnObject(409, message='Customer already exist.')
            
            #date should be in ISO format (YYYY-MM-DD)
            #grab only the date with a regex, or abort if it's not a date format
            try:
                dateRGX = '....-..-..'
                args['check_in'] = re.search(dateRGX, args['check_in']).string
                args['check_out'] = re.search(dateRGX, args['check_out']).string
            except AttributeError as e:
                return getReturnObject(400, message='BAD DATE INPUT: One or both of the dates are not in ISO format (YYYY-MM-DD).')
            
            
            customer = CUSTOMER(customer_id=None, 
                                customer_name=args['customer_name'], 
                                number_of_people=args['number_of_people'], 
                                check_in=args['check_in'], 
                                check_out=args['check_out'], 
                                price_per_night=args['price_per_night'],
                                room_id=args['room_id'],
                                booking_type=args['booking_type'],
                                comment=args['comment'],
                                stay_days_number=args['stay_days_number'])
            
            db.session.add(customer)
            db.session.commit()
            
            return getReturnObject(201, message='PUT operation completed successfully.', customer=customer)
        
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
    
    elif request.method == 'PATCH':
        #HINT: use setattr()
        try: 
            args = schemaCustomer.loads(JSONdata)
            
            result = constructDBQuery(CUSTOMER, args['filters']).all()
            
            attrs = CUSTOMER.__dir__()
            for item in result:
                for k, v in args.items():
                    if k not in attrs:
                        continue
                    setattr(item, k, v)
            
            db.session.commit()
            return getReturnObject(200, message='PATCH operation successful.', customer=result) 
                
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
    
    elif request.method == 'GET':
        try: 
            args = schemaCustomer.loads(JSONdata)
            
            result = constructDBQuery(CUSTOMER, args['filters']).all()
            
            return getReturnObject(200, customer=result)
        
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)
    
    elif request.method == 'DELETE':
        try: 
            args = schemaCustomer.loads(JSONdata)
            result = constructDBQuery(CUSTOMER, args['filters']).all()
            
            for item in result:
                db.session.delete(item)
            db.session.commit()
            
            return getReturnObject(204, message='DELETE operation successful')
            
        except marshmallow.ValidationError as e:
            return getReturnObject(400, message=e)
        
        except KeyError as e:
            message = f"BAD REQUEST: parameter \"{e.args[0]}\" not supplied"
            return getReturnObject(400, message=message)

#endregion

#endregion
