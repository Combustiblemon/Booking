from flask import Flask
from flask_restful import Api
from models.BaseModels import db
from resources import Rooms, Customers
import os.path


app = Flask(__name__)
app.app_context().push()
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

if not os.path.isfile('./database.db'):
    db.create_all()
    db.session.commit()
    print('created database file')


api.add_resource(Rooms, "/rooms/")
api.add_resource(Customers, '/customers/')


if __name__ == "__main__":
    app.run(debug=True)