import json

from flask import request, jsonify
from flask_restplus import Resource, abort

from app.main.controller import error_m
from app.main.services.brand_service import post_brand, get_brand_details, update_brand
from app.main.utils.brand_dto import BrandingDto

api = BrandingDto.api
_req_brand = BrandingDto.req_brand
_res_brand = BrandingDto.res_brand



@api.route("api/v1.0/brand")
class BrandPost(Resource):
    @api.expect(_req_brand)
    @api.marshal_with(_res_brand)
    def post(self):
        data = request.json
        return post_brand(data)


@api.route("api/v1.0/brand/<brand_id>")
class GetBrand(Resource):
    @api.marshal_with(_res_brand)
    def get(self, brand_id):
        return get_brand_details(brand_id=brand_id)


@api.route("api/v1.0/brand/update/<brand_id>")
class UpdateBrand(Resource):
    @api.expect(_req_brand)
    @api.marshal_with(_res_brand)
    def put(self, brand_id):
        data = request.json
        return update_brand(brand_id=brand_id,data=data)  
