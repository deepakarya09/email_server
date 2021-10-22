from flask_restplus import Namespace, fields


class SubscribersDto:
    api = Namespace('Subscribers')

    req_subscribers = api.model("Subscribers Info", {
        "email": fields.String(),

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