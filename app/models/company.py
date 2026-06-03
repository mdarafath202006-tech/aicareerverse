"""app/models/company.py — Company Pages"""
from datetime import datetime
from .base import db


class Company(db.Model):
    __tablename__ = "companies"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False, unique=True)
    slug        = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text)
    industry    = db.Column(db.String(100))
    website     = db.Column(db.String(255))
    logo_url    = db.Column(db.String(500))
    location    = db.Column(db.String(150))
    size        = db.Column(db.String(50))  # e.g. "1000-5000"
    founded     = db.Column(db.SmallInteger)
    is_hiring   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "slug": self.slug,
            "description": self.description, "industry": self.industry,
            "website": self.website, "location": self.location,
            "size": self.size, "is_hiring": self.is_hiring,
        }
