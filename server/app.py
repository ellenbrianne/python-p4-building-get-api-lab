#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    b_list = [b.to_dict() for b in Bakery.query.all()]
    return make_response(b_list, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id = id).first()
    if bakery:
        response = bakery.to_dict()
    return make_response(response, 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(db.desc('price')).all()
    b_list = [b.to_dict() for b in baked_goods]
    return make_response(b_list, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive = BakedGood.query.order_by(db.desc('price')).limit(1).all()
    if expensive:
        for i in expensive:
            response = i.to_dict()
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
