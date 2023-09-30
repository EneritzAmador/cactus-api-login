from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate
import jwt
import os

SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'claverandom'

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
bc = Bcrypt(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email')


user_schema = UserSchema()
multi_user_schema = UserSchema(many=True)


@app.route("/user/create", methods=["POST"])
def create_user():
    if request.content_type != "application/json":
        return jsonify("Error adding New User!")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    email = post_data.get("email")

    new_user = User(username, password, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify("User Created", user_schema.dump(new_user))


@app.route("/verify", methods=["POST"])
def verify():
    if request.content_type != "application/json":
        return jsonify("Check your format of sending Data")
    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        return jsonify("User information not verified")
    if user.password != password:
        return jsonify("User information not verified")

    return jsonify("User Verified")

@app.route("/login", methods=["POST"])
def login():
    if request.content_type != "application/json":
        return jsonify({"error": "Check your format of sending Data"}), 400

    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.email == email).first()

    if user is None or user.password != password:
        return jsonify({"error": "Usuario y/o contraseña incorrectos"}), 401

    token = jwt.encode({'user_id': user.id}, 'your_secret_key', algorithm='HS256')

    return jsonify({"token": token.decode('utf-8')}), 200




@app.route('/user/get')
def get_users():
    users = db.session.query(User).all()
    return jsonify(multi_user_schema.dump(users))

@app.route('/user/custom_login_get', methods=['GET'])
def custom_login_get_handler():
    email = request.args.get('email')
    password = request.args.get('password')

    # Verificar las credenciales del usuario y devolver una respuesta apropiada
    return jsonify({'message': 'Login successful'})

@app.route('/getusers', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify(multi_user_schema.dump(users))


@app.route('/user/delete/<id>', methods=["DELETE"])
def delete_user(id):
    delete_user = db.session.query(User).filter(User.id == id).first()
    db.session.delete(delete_user)
    db.session.commit()
    return jsonify("User Profile has been DELETED!")


@app.route('/user/update/<id>', methods=["PUT"])
def edit_user(id):
    if request.content_type != 'application/json':
        return jsonify("Send your stuff as JSON not other types!")
    put_data = request.get_json()
    username = put_data.get('username')
    email = put_data.get('email')

    edit_user = db.session.query(User).filter(User.id == id).first()

    if username != None:
        edit_user.username = username
    if email != None:
        edit_user.email = email

    db.session.commit()
    return jsonify("User Information Has Been Updated!")


@app.route('/user/editpw/<id>', methods=["PUT"])
def edit_pw(id):
    if request.content_type != 'application/json':
        return jsonify("Error updating PW")
    password = request.get_json().get("password")
    user = db.session.query(User).filter(User.id == id).first()
    user.password = password


    db.session.commit()

    return jsonify("Password Changed Successfully", user_schema.dump(user))

@app.route('/welcome')
def welcome():
    return 'Tu API funciona!! ¡Bienvenido a Login Cactus'

@app.route('/')
def index():
    return '¡Hola! Esta es la página principal d emi API cactus.'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)