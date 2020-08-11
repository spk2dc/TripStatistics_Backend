import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import login_required

# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
map = Blueprint('maps', 'map', url_prefix='/api/v1/maps')

@map.route('/', methods=["GET"])
# @login_required
def get_all_maps():
    ## find the maps and change each one to a dictionary into a new array
    try:
        maps = [model_to_dict(map) for map in models.map.select()]
        print(maps)
        return jsonify(data=maps, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@map.route('/', methods=["POST"])
# @login_required
def create_maps():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    map = models.map.create(**payload)
    ## see the object
    print(map.__dict__)
    ## Look at all the methods
    print(dir(map))
    # Change the model to a dict
    print(model_to_dict(map), 'model to dict')
    map_dict = model_to_dict(map)
    return jsonify(data=map_dict, status={"code": 201, "message": "Success"})

@map.route('/<id>', methods=["GET"])
# @login_required
def get_one_map(id):
    print(id, 'reserved word?')
    map = models.map.get_by_id(id)
    print(map.__dict__)
    return jsonify(data=model_to_dict(map), status={"code": 200, "message": "Success"})

@map.route('/<id>', methods=["PUT"])
# @login_required
def update_map(id):
    payload = request.get_json()
    query = models.map.update(**payload).where(models.map.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.map.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

@map.route('/<id>', methods=["Delete"])
# @login_required
def delete_map(id):
    query = models.map.delete().where(models.map.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})