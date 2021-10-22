from app.main.model.user import User
from app.main.model.brands import Brand
from re import TEMPLATE
from werkzeug.exceptions import BadRequest
from flask import render_template
from app.main import config, create_app ,db
from flask_mail import Mail, Message
import uuid
import base64
from itsdangerous import URLSafeTimedSerializer

auth_s = URLSafeTimedSerializer(config.Config.SECRET_KEY,"auth")


app = create_app('prod')
mail = Mail(app)

def send_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            BadRequest("user not found")
        email = email
        uui = str(user.id)
        message_bytes = uui.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        tok = base64_bytes.decode('ascii')
        token = f"{tok}_{uuid.uuid4()}"
        # token = uui.encode('ascii')
        msg = Message('Confirm Email', sender='admin@pwc.com', recipients=[email])
        link = f"{config.EMAIL_VERIFICATION_DOMAIN}{token}"
        msg.body = 'Your link is {}'.format(link)
        msg.html = render_template('email_1.html',elink=link)
        mail.send(msg)
        return {
            "message":"sended"
        }
    except Exception as e:
        raise BadRequest(f"Message not Sended due to {e}")

def confirm_email(token):
    if token == None:
        BadRequest("Please enter token")
    tok = token.split('_')
    toke = tok[0]
    try:
        base64_bytes = toke.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        userid = message_bytes.decode('ascii')
    except Exception as e:
        raise BadRequest("URL is not valid please try again")
    try:
        uuid.UUID(userid)
    except Exception as e:
        config.logging.warning(f"api: token id : Invalid Submission Id. {e}")
        raise BadRequest("This token id not valid.")
    user = User.query.filter_by(id=userid).first()
    if not user:
        raise BadRequest("URL is not valid")
    user.verified = True
    db.session.commit()
    if user.verified == True:
        return {
            "message": "Your account is already verified"
        }
    return {
        "message":"verified"
    }