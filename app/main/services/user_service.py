from app.main.services.user_registration_confirmation_mail import send_email
import calendar
from http import HTTPStatus

import base64
import hashlib
import os
import time
import uuid
from flask import request
from google.auth.transport import requests
from google.oauth2 import id_token
from password_validation import PasswordPolicy
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from app.main import config ,db
from app.main.model.user import User
from app.main.model.user_credentials import UserCredentials
from app.main.model.user_session import UserSession

policy = PasswordPolicy(uppercase=1, min_length=8, symbols=1)


def sign_up(data):
    user = User.query.filter_by(email=data['email']).first()
    if user:
        if user.login_type == "system":
            raise BadRequest(f"{user.email} already exists. Please login with email and password.")
        if user.login_type == "google":
            raise BadRequest(f"{user.email} already exists. Please login with Google.")
    create_new_id = uuid.uuid4()
    try:
        if data["login_type"] == "system":
            if "password" not in data.keys() :
                raise Unauthorized("! Please enter the password")
            if not policy.validate(data['password']):
                raise Unauthorized("! Password should contain atleast 8 characters with one uppercase letter, and one special character.")
            if "first_name" in data.keys():
                fname = data["first_name"]
            else:
                fname = ""
            if "last_name" in data.keys():
                lname = data["last_name"]
            else:
                lname = ""
            if "image_url" in data.keys():
                img = data["image_url"]
            else:
                img = "https://static.thenounproject.com/png/363633-200.png"

            try:
                user = User(id=create_new_id,
                                    first_name = fname,
                                    last_name = lname,
                                    email=data['email'],
                                    verified = False,
                                    login_type=data["login_type"],
                                    image_url=img)
            except Exception as e:
                config.logging.critical(f"! Failed to signup: {e}")
                raise Exception(f"! Failed to signup {e}")
            password = data['password']
            salt = os.urandom(16)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()
            salt = base64.b64encode(salt).decode()
            password = salt + "$" + key
            user_cred = UserCredentials(password=password, cred=user)
            db.session.add(user)
            db.session.add(user_cred)
            db.session.commit()
            return response(user, token_build(user)), HTTPStatus.OK
        elif data["login_type"] == "google":
            verify_token(data['token'])
            try:
                use = User(id=create_new_id,
                                    first_name=data['first_name'],
                                    last_name=data['last_name'],
                                    email=data['email'],
                                    verified = True,
                                    login_type=data["login_type"],
                                    image_url=data["image_url"])
            except Exception as e:
                config.logging.critical(f"Failed to signup using Google: {e}")
                raise Exception("! Failed to signup using Google. Please try again or try with email & password")
            db.session.add(use)
            db.session.commit()
            return response(use, token_build(use)), HTTPStatus.OK
        else:
            raise BadRequest("Please check login type.")
    except Exception as e:
        raise BadRequest(f"{e.description}")
    



def token_build(user):
    if user.login_type == "system":
        if user.verified == False:
                send_email(user.email)
    sub_key = os.urandom(16)
    session_uuid = uuid.uuid4()
    userId = str(user.id)
    sessionId = str(session_uuid)

    part1 = base64.b64encode(sessionId.encode()).decode()
    part2 = hashlib.sha512((userId[::-1]).encode()).hexdigest()
    part3 = base64.b64encode(sub_key).decode()

    token = part1 + "." + part2 + "." + part3
    try:
        create_session = UserSession(session_id=session_uuid, token=token,
                                 expires_at=calendar.timegm(time.gmtime()) + 86400, session=user)

        db.session.add(create_session)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        config.logging.critical(f"! Failed to generate user token : {e}")
        raise BadRequest(f"! Failed to generate user token : {e}")
    try:
        return {
        "id":user.id,
        "token": token,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "image_url":user.image_url,
        "email": user.email,
        "verified": user.verified,
        "login_type":user.login_type,
        "role": user.role,
        "first_brand_exists": user.first_brand_exists,
        "session_id": sessionId
        }
    except Exception as e:
        config.logging.critical(f"! Failed to generate user token : {e}")
        raise BadRequest("! Failed to generate user token")


def sign_in(data):
    user = User.query.filter_by(email=data['email']).first()
    if data['login_type'] != 'system':
        if data['login_type'] == "google":
            verify_token(data['token'])
        else:
            # apple login verification #
            pass
        return response(user, token_build(user))
    if not "password" in data:
        raise BadRequest("Please enter password!")
    password = data['password']

    if not policy.validate(data['password']):
        raise BadRequest("Wrong password. ! Please enter valid password.")

    if not user:
        raise BadRequest("You are not a valid user. Please create account.")

    userCred = UserCredentials.query.filter_by(id=user.id).first()
    salt, hash_password = userCred.password.split("$")
    salt = salt.encode()
    salt = base64.b64decode(salt)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

    if key != hash_password:
        raise Unauthorized("Wrong password. ! Please enter valid password.")
    return token_build(user)


def logout():
    headers = request.headers
    bearer = headers.get('Authorization')
    if not bearer:
        raise Forbidden("User is not authorized please login before logout")
    token = bearer.split()[1]
    sess = UserSession.query.filter_by(token=token).first()
    if not sess:
        raise Forbidden("Invalid user please try again.")
    db.session.delete(sess)
    db.session.commit()
    return {"message": "User logged out successfully"}, HTTPStatus.OK


def verify_token(token):
    try:
        info = id_token.verify_oauth2_token(token, requests.Request())
        if info['aud'] not in [config.EXTENSION_CLIENT_ID_PRODUCTION,config.CLIENT_ID_PRODUCTION,config.CLIENT_ID_DEVELOPMENT,config.EXTENSION_CLIENT_ID_DEVELOPMENT]:
            raise BadRequest("Google token verification failed, Please Login again with google")
    except ValueError as e:
        config.logging.critical(f"{e}")
        raise BadRequest("Google token verification failed, Please Login again with google")


def response(user, token_data):
    # NOT used join query because it heavy in processing and takes more time
    user.token = token_data["token"]
    user.session_id = token_data["session_id"]
    return user


def login(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        config.logging.warning(f"{user.email} not in our system: Please create account")
        raise BadRequest(f"{user.email} not in our system: Please create account")
        
    if data["login_type"] != 'system':
        if data["login_type"] == "google":
            verify_token(data['token'])
        return response(user, token_build(user))
    
    if data['login_type'] == "system":
        if str(user.login_type) == "google":
            raise BadRequest("Account already exists, please use google to login.")
        if not "password" in data:
            raise BadRequest("Please enter password!")
        password = data['password']
        if not policy.validate(password):
            raise BadRequest("! Password is not valid.")
        try: 
            userCred = UserCredentials.query.filter_by(id=user.id).first()
            salt, hash_password = userCred.password.split("$")
            salt = salt.encode()
            salt = base64.b64decode(salt)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()
            if key != hash_password:
                raise Unauthorized("! Password doesn't match.")
            return token_build(user)
        except:
            raise BadRequest("Not able to signin at this movement. Please check email and password")   
