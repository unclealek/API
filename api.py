from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    
    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, help="Input your name", required=True)
user_args.add_argument("email", type=str, help="Input your email", required=True)



userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users=UserModel.query.all()
        return users, 200
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
    
 
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Could not find user")
        return user, 200
    
    @marshal_with(userFields)
    def put(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if user: 
            abort(409, message= "id already taken")
        new_users = UserModel(id=id, name = args['name'], email=args['email'])
        db.session.add(new_users)
        db.session.commit()
        return new_users, 201
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message= "User doesn't exist, cannot update")
        user.name = args['name']
        user.email = args['email']     
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message= "User doesn't exist, cannot update") 
        db.session.delete(user)   
        db.session.commit()
        users = UserModel.query.all()
        return users, 204

api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')


@app.route('/')
def home():
    return "<hi>FLASK REST API</h1>"

if __name__ == '__main__':
    app.run(debug=True)