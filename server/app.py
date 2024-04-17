#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers = [camper.to_dict(only=('id', 'name', 'age')) for camper in Camper.query.all()]
        return campers, 200
    def post(self):
        try:
            json = request.get_json()
            camper = Camper(
                name=json['name'],
                age=json['age']
            )
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(only=('id', 'name', 'age')), 200
        except:
            return {"errors": ["validation errors"]}, 400
    
class CampersId(Resource):
    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).first()
        if camper:
            return camper.to_dict(), 200
        else:
            return {"error": "Camper not found"}, 404
    def patch(self, id):
        try:
            json = request.get_json()
            camper = Camper.query.filter(Camper.id == id).first()
            if camper:
                camper.name = json['name']
                camper.age = json['age']
                db.session.commit()
                return camper.to_dict(), 202
            else:
                return {"error": "Camper not found"}, 404
        except:
            return {"errors": ["validation errors"]}, 400

class Activities(Resource):
    def get(self):
        activities = [activity.to_dict(only=('id', 'name', 'difficulty')) for activity in Activity.query.all()]
        return activities, 200

class ActivitiesId(Resource):
    def get(self, id):
        activity = Activity.query.filter(Activity.id == id).first()
        if activity:
            return activity.to_dict(), 200
        else:
            return {"error": "Camper not found"}, 404
        
    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "Activity not found"}, 404
        
class Signups(Resource):
    def post(self):
        json = request.get_json()
        try:
            signup = Signup(
                camper_id=json['camper_id'],
                activity_id=json['activity_id'],
                time=json['time']
            )
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(), 201
        except:
            return { "errors": ["validation errors"] }, 400
            
    
api.add_resource(Campers, '/campers')
api.add_resource(CampersId, '/campers/<int:id>')
api.add_resource(Activities, '/activities')
api.add_resource(ActivitiesId, '/activities/<int:id>')
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
