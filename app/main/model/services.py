from sqlalchemy.dialects.postgresql import UUID
from app.main import db


class Services(db.Model):
    __tablename__ = "services"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey("brands.id"), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(db.BIGINT)
    updated_at = db.Column(db.BIGINT, nullable=True)