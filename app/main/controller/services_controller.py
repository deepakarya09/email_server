import json

from flask import request
from flask_restplus import Resource
from app.main.services.service import get_service_details, post_service, update_service
from app.main.utils.service_dto import ServiceDto

api = ServiceDto.api
_req_service = ServiceDto.req_service
_res_service = ServiceDto.res_services
_res_all_service = ServiceDto.res_all_service



@api.route("api/v1.0/brand/service")
class ServicePost(Resource):
    @api.expect(_req_service)
    @api.marshal_with(_res_service)
    def post(self):
        data = request.json
        return post_service(data)


@api.route("api/v1.0/brand/service/<service_id>")
class GetService(Resource):
    @api.marshal_with(_res_service)
    def get(self, service_id):
        return get_service_details(service_id=service_id)
    
    @api.expect(_req_service)
    @api.marshal_with(_res_service)
    def put(self, service_id):
        data = request.json
        return update_service(service_id=service_id,data=data)
     