# server/models.py

from app import db

class Sweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class VendorSweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweet.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    sweet = db.relationship('Sweet', backref='vendor_sweets')
    vendor = db.relationship('Vendor', backref='vendor_sweets')

    # Add validations
    def validate(self):
        errors = []
        if self.price is None:
            errors.append("Price must have a value")
        elif self.price < 0:
            errors.append("Price cannot be negative")
        return errors
