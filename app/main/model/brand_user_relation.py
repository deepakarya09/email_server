from sqlalchemy.dialects.postgresql import UUID
from app.main import db


class BrandUserRelation(db.Model):
    __tablename__ = "branduserrelation"
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey('brands.id'), primary_key=True)

    db.UniqueConstraint('user_id', 'brand_id')
    db.relationship('User', uselist=False, backref='memberships', lazy='dynamic')
    db.relationship('Brand', uselist=False, backref='memberships', lazy='dynamic')