import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError
from starter_code.security import authenicate, identity
from starter_code.db import db
from starter_code.resources.item import Item, ItemList
from starter_code.resources.store import Store, StoreList
from starter_code.resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose123'
api = Api(app)
db.init_app(app)
jwt = JWT(app, authenicate, identity)    # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Authentication failed: ' + err.description}), 401


if __name__ == '__main__':
    if app.config['DEBUG']:
        def create_tables():
            db.create_all()
        app.before_request(create_tables)

    app.run(port=5000)

