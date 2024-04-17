#!/usr/bin/env python3

from app import app
from models import db, Activity, Signup, Camper

with app.app_context():
    import ipdb; ipdb.set_trace()
    activity1 = Activity.query.first()
    camper1 = Camper.query.first()
    signup1 = Signup.query.first()
    import ipdb; ipdb.set_trace()
    campers = Camper.query.all()