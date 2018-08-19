from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, City, Architecture

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///city.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state token
# Store it in the session
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')


# Show all cities
@app.route('/')
@app.route('/cities/')
def showCities():
    cities = session.query(City).order_by(City.id)
    return render_template('cities.html', cities=cities)

@app.route('/cities/<int:city_id>/edit/', methods=['GET', 'POST'])
def editCity(city_id):
    editCity = session.query(City).filter_by(id=city_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editCity.name = request.form['name']
            session.commit()
        if request.form['description']:
            editCity.description = request.form['description']
            session.commit()
        return redirect(url_for('showCities'))
    else:
        return render_template('editcity.html', editCity=editCity)

@app.route('/cities/<int:city_id>/delete', methods=['GET', 'POST'])
def deleteCity(city_id):
    deleteCity = session.query(City).filter_by(id=city_id).one()
    if request.method == 'POST':
        session.delete(deleteCity)
        session.commit()
        return redirect(url_for('showCities'))
    else:
        return render_template('deleteCity.html', deleteCity=deleteCity)

@app.route('/cities/new', methods=['GET', 'POST'])
def newCity():
    if request.method == 'POST':
        newCity = City(name=request.form['name'], description=request.form['description'])
        session.add(newCity)
        session.commit()
        return redirect(url_for('showCities'))
    else:
        return render_template('newCity.html')


@app.route('/cities/<int:city_id>/')
@app.route('/cities/<int:city_id>/architectures/')
def showArchitectures(city_id):
    city = session.query(City).filter_by(id=city_id).one()
    architectures = session.query(Architecture).filter_by(city=city).all()
    return render_template('architectures.html', architectures=architectures, city_id=city_id, city=city)

@app.route('/cities/<int:city_id>/architectures/new/', methods=['GET', 'POST'])
def newArchitecture(city_id):
    city = session.query(City).filter_by(id=city_id).one()
    if request.method == 'POST':
        newArchitecture = Architecture(name=request.form['name'],
                                        description=request.form['description'],
                                        picture=request.form['picture'],
                                        city=city)
        session.add(newArchitecture)
        session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('newArchitecture.html', city_id=city_id)

@app.route('/cities/<int:city_id>/architectures/<int:architecture_id>/edit', methods=['GET', 'POST'])
def editArchitecture(city_id, architecture_id):
    # city = session.query(City).filter_by(id=city_id).one()
    editArchitecture = session.query(Architecture).filter_by(id=architecture_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editArchitecture.name = request.form['name']
            session.commit()
        if request.form['description']:
            editArchitecture.description = request.form['description']
            session.commit()
        # if request.form['architect']:
        #     editArchitecture.architect = request.form['architect']
        #     session.commit()
        if request.form['picture']:
            editArchitecture.picture = request.form['picture']
            session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('editArchitecture.html', architecture=editArchitecture)

@app.route('/cities/<int:city_id>/architectures/<int:architecture_id>/delete', methods=['GET', 'POST'])
def deleteArchitecture(city_id, architecture_id):
    deleteArchitecture = session.query(Architecture).filter_by(id=architecture_id).one()
    if request.method == 'POST':
        session.delete(deleteArchitecture)
        session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('deleteArchitecture.html', deleteArchitecture=deleteArchitecture)

# Api Endpoint for cities
@app.route('/api/')
@app.route('/api/cities')
def all_cities_handler():
    # Return all cities in database
    cities = session.query(City).order_by(City.id)
    return jsonify(cities = [i.serialize for i in cities])

# Api Endpoint for architectures
@app.route('/api/architectures')
def all_architectures_handler():
    # Return all architectures in database
    architectures = session.query(Architecture).order_by(Architecture.id)
    return jsonify(architectures = [i.serialize for i in architectures])

# Api Endpoint for architectures in one city
@app.route('/api/<int:city_id>/')
@app.route('/api/<int:city_id>/architectures')
def architecture_handler(city_id):
    # Return all architectures in one city in database
    city = session.query(City).filter_by(id=city_id).one()
    architectures = session.query(Architecture).filter_by(city=city).order_by(Architecture.id)
    return jsonify(architectures = [i.serialize for i in architectures])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)