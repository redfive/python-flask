from flask import render_template, request, session, send_from_directory, make_response
from porkins import app, hostname
import requests
import json

current_user = {}

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
    data = {'assertion': request.form['assertion'],
            'audience': 'http://localhost:5000'}
    resp = requests.post('https://verifier.login.persona.org/verify',
                         data=data,
                         verify=True)
 
    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)
 
        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Log the user in by setting a secure session cookie
            session.update({'email': verification_data['email']})

            # TODO: store this in a better way
            current_user['email'] = verification_data['email']

            # TODO: hand back a full json object for the user.
            return verification_data['email'];
 
    # Oops, something failed. Abort.
    abort(500)

@app.route('/auth/dropbox', methods=['GET'])
def login_dropbox():
  # Include the Dropbox SDK libraries
  from dropbox import client, rest, session
 
  # Get your app key and secret from the Dropbox developer website
  APP_KEY = 'f0bb7lauf2hwczh'
  APP_SECRET = 'rdlit805hwt3wke'

  # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
  ACCESS_TYPE = 'dropbox'

  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

  if 'dropbox_access_token' not in current_user:
    if 'dropbox_request_token' not in current_user:
      # check for an access token, if it exists, we don't need to go through the
      # request token steps
      request_token = sess.obtain_request_token()
      print request_token

      # Make the user sign in and authorize this token - using the oauth callback generates the
      # following url:
      # http://localhost:5000/auth/dropbox?uid=57802814&oauth_token=Up0mlUVL8sNH3mKC
      url = sess.build_authorize_url(request_token,oauth_callback='http://localhost:5000/auth/dropbox' )
      print url

      # need to build a response here and set the cookie on it.
      # resp = make_response(render_template(...))
      # resp.set_cookie('username', 'the username')

      resp = make_response(url)
      current_user['dropbox_request_token'] = request_token
      resp.set_cookie('dropbox_request_token', request_token)
    else:
      # we have the request token but still no access token
      #request_token = request.cookies['dropbox_request_token']
      request_token = current_user['dropbox_request_token']
      print request_token.key
      print request_token.secret

      # This will fail if the user didn't visit the above URL and hit 'Allow'
      # stash the access token for later use. It only needs to be created if
      # a) user has not ever given access
      # b) user has re-installed the app
      # c) user has revoked access via the Dropbox website
      # per docs, save the access token for a particular user and re-use
      access_token = sess.obtain_access_token(request_token)
      print "access_token:", access_token.key , " ", access_token.secret

      client = client.DropboxClient(sess)
      #print "linked account:", client.account_info()

      # store the access token in persistent storage too!

      resp = make_response("dropbox_success")
      resp.set_cookie('dropbox_access_token', access_token)
      current_user['dropbox_access_token'] = access_token

    # for when we had to get a request or access token
    return resp

  # for when we already have an access token
  return "dropbox_success - already linked"

@app.route('/content/dropbox/<path:path>', methods=['GET'])
def getDropboxFolder():
  # TODO: make the call to get the content at the path provided.
  #       probably as a subdirectory to the music folder (?)
  return "hello metadata for: " + path


