from sqlalchemy.dialects.postgresql import UUID
from app.main import db


class BrandSubscribersRelation(db.Model):
    __tablename__ = "brandsubscribersrelation"
    subscribers_id = db.Column(UUID(as_uuid=True), db.ForeignKey("subscribers.id"), primary_key=True)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey('brands.id'), primary_key=True)

    db.UniqueConstraint('subscribers_id', 'brand_id')
    db.relationship('Subscribers', uselist=False, backref='subs', lazy='dynamic')
    db.relationship('Brand', uselist=False, backref='subs', lazy='dynamic')