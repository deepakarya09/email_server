from sqlalchemy.dialects.postgresql import UUID
from app.main import db


class Brand(db.Model):
    __tablename__ = "brands"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    fqdn = db.Column(db.String(100), nullable=True, unique=True)
    description = db.Column(db.String(1000), nullable=True)
    facebook_url = db.Column(db.String(1000), nullable=True)
    twitter_url = db.Column(db.String(1000), nullable=True)
    instagram_url = db.Column(db.String(1000), nullable=True)
    logo = db.Column(db.String(1000), nullable=True)
    api_key = db.Column(db.String(1000), nullable=False)
    double_opt = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.BIGINT)
    updated_at = db.Column(db.BIGINT, nullable=True)
    physical_add =  db.Column(db.String(1000), nullable=True)