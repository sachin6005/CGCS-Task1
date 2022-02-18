from pyexpat import model
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck

app = Flask(__name__)

health = HealthCheck()

app.config['MONGODB_SETTINGS'] = {
    'db': 'MyTask-2',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField()
    branch = db.StringField()
    age = db.IntField()
    def to_json(self):
        return {"name": self.name,
                "branch": self.branch,
                "age" : self.age}

@app.route("/")
def root_path():
    return("Welcome")


@app.route('/user/', methods=['GET'])
def get_user():
    user = User.objects()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/user/', methods=['POST'])
def add_user():
    record = json.loads(request.data)
    user = User(name=record['name'],
                branch=record['branch'],
                age=record["age"])
    user.save()
    return jsonify(user.to_json())

@app.route('/user/<id>/', methods=['PUT'])
def Update_user(id):
    record = json.loads(request.data)
    user = User.objects.get_or_404(id=id)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(name=record['name'],
                    branch=record['branch'],
                    age=record["age"])
    return jsonify(user.to_json())

@app.route('/user/<id>/', methods=['DELETE'])
def delete_user(id):
    user = User.objects(id=id)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())


class Cars(db.Document):
    manufacturer = db.StringField()
    model = db.StringField()
    price = db.IntField()
    def to_json(self):
        return {"manufacturer": self.manufacturer,"model": self.model,"price" : self.price}
                
@app.route('/car/', methods=['GET'])
def get_car():
    car = Cars.objects()
    if not car:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(car.to_json())

@app.route('/car/', methods=['POST'])
def add_car():
    record = json.loads(request.data)
    car = Cars(manufacturer=record['manufacturer'],
                model=record['model'],
                price=record["price"])
    car.save()
    return jsonify(car.to_json())

@app.route('/car/<id>/', methods=['PUT'])
def Update_car(id):
    record = json.loads(request.data)
    car = Cars.objects.get_or_404(id=id)
    if not car:
        return jsonify({'error': 'data not found'})
    else:
        car.update(manufacturer=record['manufacturer'],
                    model=record['model'],
                    price=record["price"])
    return jsonify(car.to_json())

@app.route('/car/<id>/', methods=['DELETE'])
def delete_car(id):
    car = Cars.objects(id=id)
    if not car:
        return jsonify({'error': 'data not found'})
    else:
        car.delete()
    return jsonify(car.to_json())

app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

if __name__ == "__main__":
    app.run(debug=True)
