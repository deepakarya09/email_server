import base64
import calendar
import json
from sqlalchemy import or_
import time
import uuid
from http import HTTPStatus
import requests
from werkzeug.exceptions import BadRequest
from app.main import db, config
from app.main.model.brand_user_relation import BrandUserRelation
from app.main.model.brands import Brand
from app.main.model.user import User
from google.cloud import storage

storage_client = storage.Client()

def get_int_date(): return calendar.timegm(time.gmtime())

def upload_bucket(bytes_im, remote_path):
    bucket = storage_client.get_bucket(config.BUCKET_NAME)
    thumbnail_blob = bucket.blob(remote_path)
    thumbnail_blob.upload_from_string(bytes_im, content_type="image/png")

def upload_logo(image_data, file):
    try:
        image_data = base64.b64decode(image_data.split(",")[1])
    except Exception as e:
        raise BadRequest(f"Incorrect image format {e}")
    try:
        upload_bucket(bytes_im=image_data, remote_path=config.LOGO + file)
        cdn_image_link = config.bucket_base_url + config.LOGO + file
        return cdn_image_link
    except Exception as e:
        raise BadRequest(f"Error in upload image{e}")

def post_brand(data):
    if "user_id" not in data:
        raise BadRequest(f"user_id not available in data.")
    user = User.query.filter_by(id=data['user_id']).first()
    if not user:
        raise BadRequest("User not found. Please create account or try to re-login")
    new_id = uuid.uuid4()
    uui = str(new_id)
    message_bytes = uui.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    api_key = base64_bytes.decode('ascii')
    try:
        brand = Brand(id=new_id, name=data["name"], user_id=data["user_id"],
                          fqdn=data["fqdn"],
                          description=data["description"],
                          logo = upload_logo(data["logo"], str(uuid.uuid4()) + ".png"),
                          facebook_url=data["facebook_url"], twitter_url=data["twitter_url"],
                          double_opt = data["double_opt"],physical_add=data["physical_add"],
                          api_key=api_key,
                          instagram_url=data["instagram_url"], created_at=get_int_date(), updated_at=get_int_date())
        db.session.add(brand)
        db.session.commit()
    except Exception as e:
        config.logging.critical(f"Post brand failed with exception {e}")
        raise BadRequest("Failed to create new brand please check filled data again.")
    try:
        new_brand = Brand.query.filter_by(id=brand.id).first()
        if not new_brand:
            raise BadRequest("Brand is not created please create again")
        connect = BrandUserRelation(
                user_id = user.id,
                brand_id = new_brand.id,
            )
        db.session.add(connect)
        db.session.commit()
    except Exception as e:
        config.logging.critical(f"Failed to assign brand to user {e}")
        raise BadRequest("Failed to assign brand to logged in user. Please login again or create brand.")
    return brand, HTTPStatus.CREATED

def is_valid_id(brand_id, id):
    try:
        brand_id = uuid.UUID(brand_id)
    except Exception:
        raise BadRequest(f"Incorrect {id} ID!")
    return brand_id

def update_brand(brand_id, data):
    brand = Brand.query.filter_by(id=is_valid_id(brand_id, "brand"), ).first()
    if not brand:
        raise BadRequest("Brand not found in database. Please check brand id.")
    try:
        for key in data.keys():
            if getattr(brand, key) != data[key]:
                if (key == "logo"):
                    setattr(brand, key, upload_logo(
                        data[key], str(uuid.uuid4()) + ".png"))
                elif key != "logo":
                    setattr(brand, key, data[key])
                else:
                    pass
        setattr(brand, "updated_at", get_int_date())
    except Exception as e:
        config.logging.critical(f"Failed to updated widget:{e}")
        raise BadRequest("Error in updating brand. Please check given data.")
    db.session.commit()
    return brand, HTTPStatus.OK

def get_brand_details(brand_id):
    brand = Brand.query.filter_by(id=is_valid_id(brand_id, "brand")).first()
    if not brand:
        raise BadRequest("Brand not found. Please check brand id!")
    return brand, HTTPStatus.OK
