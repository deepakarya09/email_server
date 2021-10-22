from flask_restplus import Namespace, fields


class ServiceDto:
    api = Namespace('Service')

    req_service = api.model("Service Info", {
        "name": fields.String(),
        "brand_id": fields.String(),
        "description": fields.String()
    })

    res_services = api.model("Brand Return Response", {
        "id": fields.String(),
        "brand_id": fields.String(),
        "name": fields.String(),
        "description": fields.String(),
        "created_at":fields.String(),
        "updated_at":fields.String(),
    })

    res_all_service = api.model("Response all services",{
        "items":fields.List(fields.Nested(res_services))
    })