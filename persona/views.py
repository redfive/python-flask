from flask import render_template, request, session, send_from_directory, abort
from persona import app
import requests
import json

# serve some static files for local development
@app.route('/js/<path>')
@app.route('/css/<path>')
@app.route('/lib/<path>')
def static_from_root(path):
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/")
def home_page():
    response =  render_template('home.html')
    return response

@app.route("/login")
def login_page():
    response =  render_template('login.html', logged_in=False)
    return response

@app.route('/auth/logout', methods=['POST'])
def do_logout():
    # TODO: clear the session cookie, actually log out user
    return "logged out"

@app.route('/auth/login', methods=['POST'])
def do_login():
    # The request has to have an assertion for us to verify
    if 'assertion' not in request.form:
        # TODO: this may be overkill - or not for REST API
        abort(400)
 
    # Send the assertion to Mozilla's verifier service.
    data = {'assertion': request.form['assertion'], 'audience': 'http://localhost:5000'}
    resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)
 
    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)
 
        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Log the user in by setting a secure session cookie
            session.update({'email': verification_data['email']})

            # TODO: hand back a full json object for the user.
            return verification_data['email'];
 
    # Oops, something failed. Abort.
    abort(500)

