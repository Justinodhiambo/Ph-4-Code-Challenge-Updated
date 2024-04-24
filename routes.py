# routes.py

from app import app, db
from flask import jsonify, request
from models import Sweet, Vendor, VendorSweet

# Routes for sweets
@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([{"id": sweet.id, "name": sweet.name} for sweet in sweets])

@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = Sweet.query.get(id)
    if sweet:
        return jsonify({"id": sweet.id, "name": sweet.name})
    else:
        return jsonify({"error": "Sweet not found"}), 404

# Routes for vendors
@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([{"id": vendor.id, "name": vendor.name} for vendor in vendors])

@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if vendor:
        vendor_sweets = [{"id": vs.id, "price": vs.price, "sweet_id": vs.sweet_id, "vendor_id": vs.vendor_id} for vs in vendor.vendor_sweets]
        return jsonify({"id": vendor.id, "name": vendor.name, "vendor_sweets": vendor_sweets})
    else:
        return jsonify({"error": "Vendor not found"}), 404

# Routes for vendor sweets
@app.route('/vendor_sweets', methods=['POST'])
def add_vendor_sweet():
    data = request.json
    new_vendor_sweet = VendorSweet(price=data['price'], sweet_id=data['sweet_id'], vendor_id=data['vendor_id'])
    errors = new_vendor_sweet.validate()
    if errors:
        return jsonify({"errors": errors}), 400
    else:
        db.session.add(new_vendor_sweet)
        db.session.commit()
        return jsonify({"id": new_vendor_sweet.id, "price": new_vendor_sweet.price, "sweet_id": new_vendor_sweet.sweet_id, "vendor_id": new_vendor_sweet.vendor_id}), 201

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.get(id)
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({}), 204
    else:
        return jsonify({"error": "VendorSweet not found"}), 404
