from flask import Blueprint, jsonify, request
from ..models import Incident
from .. import db

api = Blueprint("api", __name__)

@api.route("/incidents", methods=["GET"])
def list_incidents():
    incidents = Incident.query.all()
    return jsonify([{"id":i.id,"title":i.title,"status":i.status} for i in incidents])

@api.route("/incidents", methods=["POST"])
def create_incident():
    data = request.json
    incident = Incident(title=data["title"], description=data.get("description"))
    db.session.add(incident)
    db.session.commit()
    return jsonify({"message":"created"}),201
