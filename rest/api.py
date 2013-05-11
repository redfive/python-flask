from rest import manager
from rest.models import User

# The class representing the underlying db model. Not positive
# this sort of inheritance is necessary but wanted to see if it
# worked. Could open the way for different apps to use the same
# User db model.
class UserAPI(User):
    api_version = '0.1'

    def __init__ (self, username, email):
        print 'Creating a UserAPI object'
        User.__init__(self, username, email)

    def validate(self, data):
        # do validation of data
        print 'UserAPI.validate'
        return True

# Create API endpoints
manager.create_api(UserAPI,
                   url_prefix = '/api/v' + UserAPI.api_version,
                   collection_name = 'users',
                   methods=['GET', 'POST', 'PUT', 'DELETE'])

# tested with these curl commands:
# curl http://localhost:5000/api/v0.1/users
# curl -X POST -H "Content-Type: application/json" -d '{"username":"bob","email":"bob@bobstractors.com"}' http://localhost:5000/api/v0.1/users
# curl -X PUT -H "Content-Type: application/json" -d '{"email":"bob@bobstractorsandtrucks.com"}' http://localhost:5000/api/v0.1/users/bob
# curl -X DELETE  http://localhost:5000/api/v0.1/users/bob
