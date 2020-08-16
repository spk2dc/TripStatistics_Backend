import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('users', 'user', url_prefix='/user')


@user.route('/register', methods=["POST"])
def register():
    # See request payload anagolous to req.body in express
    # This has all the data like username, email, password
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    print('\nregister payload: \n', payload)

    try:
        # Find if the user already exists?
        # model query finding by email
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with this email already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(
            payload['password'])  # bcrypt line for generating the hash
        user = models.User.create(**payload)  # put the user in the databaset

        # starts user session
        login_user(user)

        user_dict = model_to_dict(user)
        print('\nregistered user: \n', user_dict)
        print(type(user_dict))
        # delete the password before we return it, because we don't need the client to be aware of it
        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Register successful"})


@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    print('\nlogin payload: \n', payload)

    try:
        # Try to find the user by their email
        user = models.User.get(models.User.email == payload['email'])
        # if you find the User model convert in to a dictionary so you can edit and jsonify it
        user_dict = model_to_dict(user)
        # use bcrypt to check password and see if input password matches
        if(check_password_hash(user_dict['password'], payload['password'])):
            # delete the password since the client doesn't need it
            del user_dict['password']
            login_user(user)  # set up the session
            print('\nlogged in user is: \n', user)
            # respond to the client
            return jsonify(data=user_dict, status={"code": 200, "message": "Login successful"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "User does not exist"})


@user.route('/logout', methods=["GET"])
def logout():
    print('\nlogging out: \n', current_user)
    logout_user()
    return jsonify(data={}, status={'code': 200, 'message': 'Successful logout'})
