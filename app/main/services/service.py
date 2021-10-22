import base64
import calendar
import json
from sqlalchemy import or_
import time
import uuid
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from app.main import db, config
from app.main.model.brand_user_relation import BrandUserRelation
from app.main.model.brands import Brand
from app.main.model.services import Services

def get_int_date(): return calendar.timegm(time.gmtime())

def post_service(data):
    if "brand_id" not in data:
        raise BadRequest(f"brand_id not available in data.")
    brand = Brand.query.filter_by(id=data['brand_id']).first()
    if not brand:
        raise BadRequest("Brand not found. Please create brand or check id")
    try:
        service = Services(id=uuid.uuid4(), name=data["name"], brand_id=data["brand_id"],
                          description=data["description"],created_at=get_int_date(), updated_at=get_int_date())
        db.session.add(service)
        db.session.commit()
    except Exception as e:
        config.logging.critical(f"Post Service failed with exception {e}")
        raise BadRequest("Failed to create new service please check filled data again.")
    return brand, HTTPStatus.CREATED

def is_valid_id(service_id, id):
    try:
        service_id = uuid.UUID(service_id)
    except Exception:
        raise BadRequest(f"Incorrect {id} ID!")
    return service_id

def update_service(service_id, data):
    service = Services.query.filter_by(id=is_valid_id(service_id, "service"), ).first()
    if not service:
        raise BadRequest("Service not found in database. Please check service id.")
    try:
        for key in data.keys():
            if getattr(service, key) != data[key]:
                setattr(service, key, data[key])
        setattr(service, "updated_at", get_int_date())
    except Exception as e:
        config.logging.critical(f"Failed to updated widget:{e}")
        raise BadRequest("Error in updating brand. Please check given data.")
    db.session.commit()
    return service, HTTPStatus.OK

def get_service_details(service_id):
    service = Services.query.filter_by(id=is_valid_id(service_id, "Service")).first()
    if not service:
        raise BadRequest("Service not found. Please check service id!")
    return service, HTTPStatus.OK
