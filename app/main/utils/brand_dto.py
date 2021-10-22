from flask_restplus import Namespace, fields


class BrandingDto:
    api = Namespace('Branding')

    req_brand = api.model("Brand Info", {
        "name": fields.String(),
        "fqdn": fields.Url(),
        "user_id": fields.String(),
        "description": fields.String(),
        "facebook_url": fields.String(default=None),
        "twitter_url": fields.String(),
        "instagram_url": fields.String(),
        "double_opt":fields.Boolean(),
        "physical_add":fields.String(),
        "logo": fields.String()
    })

    res_brand = api.model("Brand Return Response", {
        "id": fields.String(),
        "user_id": fields.String(),
        "fqdn": fields.Url(),
        "name": fields.String(),
        "description": fields.String(),
        "facebook_url": fields.String(),
        "twitter_url": fields.String(),
        "instagram_url": fields.String(),
        "created_at": fields.String(),
        "updated_at": fields.String(),
        "double_opt":fields.Boolean(),
        "physical_add":fields.String(),
        "logo": fields.String(),
        "api_key":fields.String(),
    })
