from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    url_for,
    flash,
    make_response
)
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, City, Architecture
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import random
import string

app = Flask(__name__)

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
    """
    Shows login page
    """
    if 'access_token' in login_session:
        return redirect(url_for('showCities'))
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, CLIENT_ID=CLIENT_ID)


@app.route('/logout')
def logout():
    """
    Delete access_token and redirect to login page
    """
    login_session.pop('access_token', None)
    return redirect(url_for('showLogin'))


# Google sign-in
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
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; ' \
              'border-radius: 150px;-webkit-border-radius: ' \
              '150px; -moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    # If user is not in database, register.
    try:
        user = session.query(User).filter_by(email=login_session[
    'email']).one()
    except:
        newUser = User(name=login_session['username'],
                        email=login_session['email'])
        session.add(newUser)
        session.commit()
    return output


@app.route('/')
@app.route('/cities/')
def showCities():
    """
    Shows all cities in the database
    """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    cities = session.query(City).order_by(City.id)
    return render_template('cities.html', cities=cities)


@app.route('/cities/new', methods=['GET', 'POST'])
def newCity():
    """
    Creates city information to the database
    :return:
        on GET: Page to create city
        on Post: Redirect to main page after city has been created
    """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(email=login_session[
        'email']).one()
    if request.method == 'POST':

        newCity = City(name=request.form['name'],
                   description=request.form['description'],
                       user=user)
        session.add(newCity)
        session.commit()
        return redirect(url_for('showCities'))
    else:
        return render_template('newCity.html')


@app.route('/cities/<int:city_id>/edit/', methods=['GET', 'POST'])
def editCity(city_id):
    """
    Edits city information in the database
    :param city_id:
    :return:
        on GET: Page to edit city
        on Post: Redirect to main page after city has been edited
    """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(email=login_session[
        'email']).one()
    editCity = session.query(City).filter_by(id=city_id).one()
    if user.id != editCity.user_id:
        flash("You are not allowed to edit %s" % editCity.name)
        return redirect(url_for('showCities'))
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
    """
    Deletes city information in the database
    :param city_id:
    :return:
        on GET: Page to confirm for deleting city
        on Post: Redirect to main page after city has been deleted
    """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(email=login_session[
        'email']).one()
    deleteCity = session.query(City).filter_by(id=city_id).one()
    if user.id != deleteCity.user_id:
        flash("You are not allowed to delete %s" % deleteCity.name)
        return redirect(url_for('showCities'))
    if request.method == 'POST':
        session.delete(deleteCity)
        session.commit()
        return redirect(url_for('showCities'))
    else:
        return render_template('deleteCity.html', deleteCity=deleteCity)


@app.route('/cities/<int:city_id>/')
@app.route('/cities/<int:city_id>/architectures/')
def showArchitectures(city_id):
    """
    Shows all architectures in selected city in the database
    :param city_id:
    """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    city = session.query(City).filter_by(id=city_id).one()
    architectures = session.query(Architecture).filter_by(city=city).all()
    return render_template('architectures.html', architectures=architectures,
                           city_id=city_id, city=city)


@app.route('/cities/<int:city_id>/architectures/new/', methods=['GET', 'POST'])
def newArchitecture(city_id):
    """
    Creates architecture in selected city to the database
    :param city_id:
    :return:
        on GET: Page to create architecture
        on Post: Redirect to city page after architecture has been created
    """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(email=login_session[
        'email']).one()
    city = session.query(City).filter_by(id=city_id).one()
    if user.id != city.user_id:
        flash("You are not allowed to add architecture in this city")
        return redirect(url_for('showArchitectures', city_id=city_id))
    if request.method == 'POST':
        newArchitecture = Architecture(name=request.form['name'],
                                       description=request.form['description'],
                                       picture=request.form['picture'],
                                       city=city,
                                       user=user)
        session.add(newArchitecture)
        session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('newArchitecture.html', city_id=city_id)


@app.route('/cities/<int:city_id>/architectures/<int:architecture_id>/edit',
           methods=['GET', 'POST'])
def editArchitecture(city_id, architecture_id):
    """
        Edits architecture in selected city in the database
        :param city_id:
        :return:
            on GET: Page to edit architecture
            on Post: Redirect to city page after architecture has been edited
        """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(email=login_session[
        'email']).one()
    city = session.query(City).filter_by(id=city_id).one()
    editArchitecture = session.query(Architecture).filter_by(
        id=architecture_id).one()
    if user.id != city.user_id:
        flash("You are not allowed to edit %s" % editArchitecture.name)
        return redirect(url_for('showArchitectures', city_id=city_id))
    if request.method == 'POST':
        if request.form['name']:
            editArchitecture.name = request.form['name']
            session.commit()
        if request.form['description']:
            editArchitecture.description = request.form['description']
            session.commit()
        if request.form['picture']:
            editArchitecture.picture = request.form['picture']
            session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('editArchitecture.html',
                               architecture=editArchitecture)


@app.route('/cities/<int:city_id>/architectures/<int:architecture_id>/delete',
           methods=['GET', 'POST'])
def deleteArchitecture(city_id, architecture_id):
    """
        Delete architecture in selected city in the database
        :param city_id:
        :return:
            on GET: Page to delete architecture
            on Post: Redirect to city page after architecture has been deleted
        """
    if 'access_token' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(email=login_session[
        'email']).one()
    city = session.query(City).filter_by(id=city_id).one()
    deleteArchitecture = session.query(Architecture).filter_by(
        id=architecture_id).one()
    if user.id != city.user_id:
        flash("You are not allowed to delete %s" % deleteArchitecture.name)
        return redirect(url_for('showArchitectures', city_id=city_id))
    if request.method == 'POST':
        session.delete(deleteArchitecture)
        session.commit()
        return redirect(url_for('showArchitectures', city_id=city_id))
    else:
        return render_template('deleteArchitecture.html',
                               deleteArchitecture=deleteArchitecture)


# Api Endpoint for cities
@app.route('/api/')
@app.route('/api/cities')
def all_cities_handler():
    # Return all cities in database
    cities = session.query(City).order_by(City.id)
    return jsonify(cities=[i.serialize for i in cities])


# Api Endpoint for architectures
@app.route('/api/architectures')
def all_architectures_handler():
    # Return all architectures in database
    architectures = session.query(Architecture).order_by(Architecture.id)
    return jsonify(architectures=[i.serialize for i in architectures])


# Api Endpoint for architectures in one city
@app.route('/api/<int:city_id>/')
@app.route('/api/<int:city_id>/architectures')
def architecture_handler(city_id):
    # Return all architectures in one city in database
    city = session.query(City).filter_by(id=city_id).one()
    architectures = session.query(Architecture).filter_by(city=city).order_by(
        Architecture.id)
    return jsonify(architectures=[i.serialize for i in architectures])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
