from app.main import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    image_url = db.Column(db.String(500), nullable=True)
    verified = db.Column(db.Boolean,nullable=True,default=False)
    login_type = db.Column(db.String, nullable=True)
    user_creds = db.relationship("UserCredentials", uselist=False, backref="cred")
    rel_session = db.relationship("UserSession", backref="session",lazy=True)
