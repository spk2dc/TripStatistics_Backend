import models
import os
from flask import Flask, Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

if 'ON_HEROKU' in os.environ:
    print('\nheroku upload folder set')
    UPLOAD_FOLDER = '/tmp/'
else:
    print('\nlocal upload folder set')
    UPLOAD_FOLDER = './file_uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'json'}

# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
all_map = Blueprint('all_maps', 'all_map', url_prefix='/api/v1/all_maps')


def allowed_file(filename):
    """Check if filename is an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def print_map_small(one_map):
    """Print one map excluding location data for brevity"""
    print('print_map_small method')
    print('map.__dict__ {',
          '\n   id: ', one_map.__dict__['__data__']['id'],
          '\n   user: ', one_map.__dict__['__data__']['user'],
          '\n   filename: ', one_map.__dict__['__data__']['filename'],
          '\n   trip_name: ', one_map.__dict__['__data__']['trip_name'],
          '\n}\n')


@all_map.route('/', methods=["GET"])
@login_required
def get_all_maps():
    # find the maps and change each one to a dictionary into a new array
    try:
        print('\nget all maps for user: \n', current_user.get_id())
        all_maps = [model_to_dict(map) for map in current_user.all_maps]
        # print('\nget all maps: \n', all_maps)
        return jsonify(data=all_maps, status={"code": 200, "message": "Get all maps successful"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting all maps"})


@all_map.route('/', methods=["POST"])
@login_required
def create_maps():
    # retrieve file and save name securely
    fileInp = request.files['data']
    if allowed_file(fileInp.filename):
        filename = secure_filename(fileInp.filename)
        fileInp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return jsonify(data={}, status={"code": 401, "message": "Error saving file"})

    # move pointer to beginning of file after it was saved
    fileInp.stream.seek(0)
    # read from file and store as string
    fileString = fileInp.read().decode('utf8')
    # store in payload to create entry in database
    print('\ncreate map for user: \n', request.form['user'])
    payload = {
        "trip_name": request.form['trip_name'],
        "filename": request.form['filename'],
        "user": request.form['user'],
        "data": fileString
    }
    print('\ncreate map payload { \n',
          payload['user'], payload['filename'], payload['trip_name'], '\n\npayload data[:500] is \n', payload['data'][:500], '\n}  end create map payload\n')
    new_map = models.All_Map.create(**payload)
    # see the object
    print_map_small(new_map)
    # Look at all the methods
    # print('\npayload methods: \n', dir(new_map))
    # Change the model to a dict
    map_dict = model_to_dict(new_map)
    map_dict['data'] = map_dict['data'][:500] + \
        '\n*****location data truncated for printing*****\n'
    print('\nnew_map model to dict: \n', map_dict)
    return jsonify(data=map_dict, status={"code": 201, "message": "Create maps successful"})


@all_map.route('/<id>', methods=["GET"])
@login_required
def get_one_map(id):
    print('\nget map id: ', id)
    one_map = models.All_Map.get_by_id(id)
    print_map_small(one_map)
    return jsonify(data=model_to_dict(one_map), status={"code": 200, "message": "Get one map successful"})


@all_map.route('/<id>', methods=["PUT"])
@login_required
def update_map(id):
    print('\nupdate map id: ', id)
    payload = request.get_json()
    query = models.All_Map.update(**payload).where(models.All_Map.id == id)
    query.execute()
    return jsonify(data=model_to_dict(models.All_Map.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})


@all_map.route('/<id>', methods=["Delete"])
@login_required
def delete_map(id):
    print('\ndelete map id: ', id)
    query = models.All_Map.delete().where(models.All_Map.id == id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

# Sources:
# https://pythonbasics.org/flask-upload-file/
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
# https://www.twilio.com/blog/working-with-json-in-python
# https://stackoverflow.com/questions/16603621/how-to-store-json-object-in-sqlite-database
# https://www.sqlite.org/json1.html
# https://stackoverflow.com/questions/28438141/python-flask-upload-file-but-do-not-save-and-use
