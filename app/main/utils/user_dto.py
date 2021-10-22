from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')

    req_user_info = api.model("request Signup", {
        'first_name': fields.String(required=False, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'image_url': fields.String(required=False),
        'login_type': fields.String(required=True),
        'email': fields.String(required=True, description='email address'),
        'password': fields.String(required=False, description='password'),
        "token": fields.String()
    })

    req_email_verification = api.model("request email", {
        'email': fields.String(required=True, description='email')
    })

    login_request = api.model("Login", {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
        "image_url": fields.Url(),
        "login_type": fields.String(),
        "token": fields.String(),
        "password":fields.String()
    })
    login_response = api.model("Login Response",{
        "id": fields.String(),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
        "image_url": fields.String(),
        "token": fields.String(),
        "verified":fields.Boolean(description='Verification of user'),
        "login_type": fields.String(attribute="login_type"),
        "first_brand_exists": fields.Boolean(),
        "session_id": fields.String(),
        
    })

    res_user_info = api.model("response Signup", {
        "id": fields.String(desription="uuid"),
        'first_name': fields.String(description='first name'),
        'last_name': fields.String(description='last name'),
        "image_url":fields.String(description="image link"),
        'email': fields.String(description='email address'),
        "verified":fields.Boolean(description='Verification of user'),
        "first_brand_exists": fields.Boolean(description='if false then send to welcome page else dashboard'),
        "token": fields.String(),
        "session_id": fields.String(attribute="session_id")
    })

    req_user_auth = api.model("request signing", {
        "email": fields.String(required=True, description='user mail id'),
        "password": fields.String(required=True, description='password'),
    })

    return_sign_in = api.model("Login Response", {
        "token": fields.String(),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
        "session_id": fields.String(attribute="session_id")
    })
