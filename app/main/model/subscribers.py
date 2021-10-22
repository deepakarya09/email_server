from sqlalchemy.dialects.postgresql import UUID
from app.main import db


class Subscribers(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    status = db.Column(db.String(200), nullable=False, unique=True)
    system_type = db.Column(db.String(200), nullable=False, unique=True)
    confirmation = db.Column(db.Boolean, default=True)
    submitted_at = db.Column(db.BIGINT)
    ip_address = db.Column(db.String(200), nullable=False, unique=True)
    service_type = db.Column(UUID(as_uuid=True), db.ForeignKey("services.id"), nullable=False)