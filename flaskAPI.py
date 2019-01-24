from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, join, select
#sessions?
#MetaData?
#Mapper (using models to represent tables)
#deployment
#flask Get and Post
#jsonify

app = Flask(__name__)
api = Api(app)
engine = create_engine('mysql+pymysql://root:root@localhost:8889/fifa18players')
conn = engine.connect()
metadata = MetaData()
countries = Table('countries', metadata, autoload = True, autoload_with = engine)
continents = Table('continents', metadata, autoload = True, autoload_with = engine)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/fifa18players'
# db = SQLAlchemy(app)
# class players(db.Model):
#     __tablename__ = 'players'
#     id = db.Column('id', db.Integer, primary_key = True)
#     name = db.Column('name', db.Unicode)
#     age = db.Column('age', db.Unicode)
#     nationality = db.Column('nationality', db.Unicode)
#     fifa_score = db.Column('fifa_score', db.Unicode)
#     club = db.Column('club', db.Unicode)
#     value = db.Column('value', db.Unicode)
#     salary = db.Column('salary', db.Unicode)


@app.route('/')
def index():
    return "Please Write the country name you want It's continent to be returned"

# @app.route('/continents')
# def get_continents():
#     return repr(continents)
#
# @app.route('/countries')
# def get_countries():
#     return repr(countries)

@app.route('/<country_name>', methods=['GET', 'POST'])
def get_coutry_continent(country_name):
    continents_join_countries = continents.join(countries)
    query = select([continents]).select_from(continents_join_countries).where("countries.name = '%s'" % country_name)
    result = conn.execute(query)
    json_data=[]
    for row in result:
        json_data.append(dict(row))
    return jsonify(json_data)


@app.route('/getAll', methods=['GET', 'POST'])
def getAll():
    continents_join_countries = continents.join(countries)
    query_result = conn.execute("select countries.name as country, continents.name as continent from continents join countries ON countries.continent_code = continents.code")
    json_data=[]
    for row in query_result:
        json_data.append(dict(row))
    return jsonify(json_data)



if __name__ == '__main__':
    app.run(debug=True)
