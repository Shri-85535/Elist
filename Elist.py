import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akash:Myoxyblue35!@localhost/temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'User_List'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Employee(db.Model):
    __tablename__ = 'Employee_List'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
class E_schema(ma.Schema):
    class Meta:
        fields = ('name','email')

db.create_all()
ESchema = E_schema()
EsSchema = E_schema(many=True)


@auth.verify_password
def verify_password(name, password):
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        print("User Not Found!")
    elif not user.verify_password(password):
        print("Unable to verify password")
        return False
    else:
        g.name = name
        return True

@app.route('/userlist', methods=['POST'])
def add_user():
    name = request.json['name']
    password = request.json['password']
    if name is None or password is None:
        print("Missing Arguments")
        abort(400)
        
    user = db.session.query(User).filter_by(name=name).first()
    if user is not None:
        print("Existing User")
        return jsonify({"Message":"User already exist"}),200
    newuser = User(name=name)
    newuser.hash_password(password)
    db.session.add(newuser)
    db.session.commit()
    return jsonify({"name":newuser.name}), 201

@app.route('/elist', methods=['POST'])
def add_emp():
    name = request.json['name']
    email = request.json['email']
    
    new_emp = Employee(name, email)
    db.session.add(new_emp)
    db.session.commit()
    
    Emp = Employee.query.get(new_emp.id)
    return ESchema.jsonify(Emp)

@app.route('/')
@app.route('/elist', methods=['GET'])
@auth.login_required
def show_emps():
    all_emp = Employee.query.all()
    result = EsSchema.dump(all_emp)
    return jsonify(result.data)

@app.route('/elist/<id>', methods=['GET'])
def emp_byid(id):
    empbyid = Employee.query.get(id)
    return ESchema.jsonify(empbyid)

@app.route('/elist/<id>', methods=['PUT'])
def edit_byid(id):
    editbyid = Employee.query.get(id)
    
    name = request.json['name']
    email = request.json['email']
    
    editbyid.name = name
    editbyid.email = email
    db.session.commit()
    return ESchema.jsonify(editbyid)

@app.route('/elist/<id>', methods=['DELETE'])
def del_byid(id):
    delbyid = Employee.query.get(id)
    db.session.delete(delbyid)
    db.session.commit()
    return ESchema.jsonify(delbyid)

if __name__ == '__main__':
    app.run(debug=True)
