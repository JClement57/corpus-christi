import json
import os
from datetime import datetime, timedelta

from flask import request, send_file, url_for, redirect
from werkzeug.utils import secure_filename
from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, jwt_optional
from flask_mail import Message
from marshmallow import ValidationError
from sqlalchemy import func

from . import images
from .. import db, mail, BASE_DIR
from ..etc.helper import modify_entity, get_exclusion_list, is_allowed_file, get_file_extension, get_hash
from .models import Image, ImageSchema, ImageEvent, ImageEventSchema

# ---- Image

image_schema = ImageSchema()
image_schema_partial = ImageSchema(partial=True)

@images.route('/<image_id>')
@jwt_required
def download_image(image_id):
    image = db.session.query(Image).filter_by(id=image_id).first()

    if not image:
        return jsonify(f"Image with id #{image_id} does not exist."), 404

    image_path = os.path.join(BASE_DIR + '/', image.path)

    return send_file(image_path, mimetype='image/jpg')


@images.route('/', methods=['POST'])
@jwt_required
def upload_image():
    # -- POST request should be sent with image in request.files['image'] &
    # description in request.form['data'] as a json object (e.g. {'description': 'this is a picture.'})
    if request.files:
        if request.files['file']:
            image = request.files['file']
        else:
            return 'No image file found in "files" section', 422
    else:
        return 'No image selected', 422

    valid_desc = None
    if request.form:
        if request.form['data']:
            data = json.loads(request.form['data'])
            try:
                valid_desc = image_schema.load(data, partial=('path', 'id'))
            except ValidationError as err:
                return jsonify(err.messages), 422

    filename = secure_filename(image.filename)

    if is_allowed_file(filename):
        file_hash = get_hash(filename)
        new_filename = file_hash + '.' + get_file_extension(filename)
        folder_path = 'data/images/'
        path_to_image = os.path.join(folder_path, new_filename)
        image_already_in_db = db.session.query(Image).filter_by(path=path_to_image).first()

        if image_already_in_db:
            return 'Image with same name already exists', 422

        full_path = os.path.join(BASE_DIR + '/', path_to_image)
        image.save(full_path)
    else:
        return 'Invalid file type', 422
    
    valid_image = dict()
    valid_image['path'] = path_to_image
    if valid_desc:
        valid_image['description'] = data['description']

    valid_image = image_schema.load(valid_image, partial=True)

    new_image = Image(**valid_image)
    db.session.add(new_image)
    db.session.commit()

    return jsonify(image_schema.dump(new_image)), 201
    

@images.route('/<image_id>', methods=['PATCH'])
@jwt_required
def update_image(image_id):
    # PATCH can only be used to update an image's description
    try: 
        valid_attributes = image_schema.load(request.json, partial=(id, path))
    except ValidationError as err:
        return jsonify(err.messages), 422
                
    return modify_entity(Image, image_schema_partial, image_id, valid_attributes)


@images.route('/<image_id>', methods=['DELETE'])
@jwt_required
def delete_image(image_id):
    image = db.session.query(Image).filter_by(id=image_id).first()
    
    if not image:
        return jsonify(f"Image with id #{image_id} does not exist."), 404

    os.remove(os.path.join(BASE_DIR, image.path))
    
    db.session.delete(image)
    db.session.commit()

    # 204 codes don't respond with any content
    return "Deleted successfully", 204




