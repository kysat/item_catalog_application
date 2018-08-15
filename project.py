from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, City, Architecture

engine = create_engine('sqlite:///city.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

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


# @app.route('/cities/<int:city_id>/')
@app.route('/cities/<int:city_id>/architectures/')
def showArchitectures(city_id):
    city = session.query(City).filter_by(id=city_id).one()
    architectures = session.query(Architecture).filter_by(city=city).all()
    return render_template('architectures.html', architectures=architectures, city_id=city_id)

@app.route('/cities/<int:city_id>/architectures/new/', methods=['GET', 'POST'])
def newArchitecture(city_id):
    city = session.query(City).filter_by(id=city_id).one()
    if request.method == 'POST':
        newArchitecture = Architecture(name=request.form['name'],
                                        description=request.form['description'],
                                        # architect=request.form['architect'],
                                        picture=request.form['picture'],
                                        city=city)
        session.add(newArchitecture)
        session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('newArchitecture.html', city_id=city_id)

@app.route('/cities/<int:city_id>/architectures/<int:architecture_id>/', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)