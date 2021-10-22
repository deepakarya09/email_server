from flask_restplus import Api
from flask import Blueprint

from app.main.controller.user_controller import api as reg_ns
from app.main.controller.brand_controller import api as brand_ctr
from app.main.controller.services_controller import api as servicers_ctr
# from app.main.controller.subscribers_controller import api as subs_ctr

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Email service',
    version='1.0',
    description='rest api in flask',
)

api.add_namespace(reg_ns, path='/')
api.add_namespace(brand_ctr, path='/')
api.add_namespace(servicers_ctr, path='/')
# api.add_namespace(subs_ctr, path='/')
