import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as pwd_context

auth = HTTPAuth()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akash:Myoxyblue35!@localhost/temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'Users':
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Employee(db.Model):
    __tablename__ = 'Employees List'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

class E_Schema(ma.Schema):
    class Meta:
        fields = ('name', 'email')
        
db.create_all()
Eshcema = E_Schema()
ESshcema = E_Schema(many=True)

@auth.verify_password()
def verify_password(name, password):
    print("looking for name %s" %name)
    name = db.session.query(User).filter_by(name=name).first()
    if not name:
        print('User not found!')
    elif not user.verify_password(password):
        print('unable to verify password')
        return False
    else:
        g.name = name
        return True

#endpoint to create new User
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    password = request.json['password']
    if name is None or password is None:
        print ("Missing Arguments")
        abort(400)
    user = db.session.query(Users).filter_by(name=name).first()
    if user is not None:
        print("existing User")
        return jsonify({'message':'user already exists'}), 200
    newuser = User(name=name)
    newuser.hash_password(password)
    db.session.add(newuser)
    db.session.commit()
    return jsonify({"name":newuser.name}), 201

#endpoint to create new employee
@app.route('/employee', methods=['POST'])
def add_emp():
    name = request.json['name']
    email = request.json['email']
    
    addemp = Employee(name, email)
    db.session.add(newemp)
    db.session.commit()
    
    newemp = Employee.query.get(addemp.id)
    return Eshcema.jsonify(newemp)

#endpoint to show all employee
@app.route('/', methods=['GET'])
@app.route('/employee', methods=['GET'])
def show_emp():
    allemp = Employee.query.all()
    result = ESschema.dump(allemp)
    return jsonify(result.data)

#endpoint to get  employee by  id
@app.route('/employee/<id>', methods=['GET'])
def emp_byid(id):
    empbyid = Employee.query.get(id)
    return Eschema.jsonify(empbyid)

#endpoint to edit  employee by  id
@app.route('/employee/<id>', methods=['PUT'])
def edit_emp(id):
    editemp = Employee.query.get(id)
    name = request.json['name']
    email = request.json['email']
    
    editemp.name = name
    editemp.email = name
    db.session.commit()
    return Eschema.jsonify(editemp)

#endpoint to delete  employee by  id
def del_emp(id):
    delemp = Employee.query.get(id)
    db.session.delete(delemp)
    db.session.commit()
    return Eschema.jsonify(delemp)

if __name__ == ('__main__'):
    app.run(debug=True)
