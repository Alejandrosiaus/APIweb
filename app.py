from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TU_CONTRASEÑA@localhost:5432/incidentes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pendiente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



# Crear nuevo incidente
@app.route('/incidents', methods=['POST'])
def create_incident():
    data = request.json
    reporter = data.get('reporter')
    description = data.get('description')

    # Validaciones
    if not reporter:
        return jsonify({"error": "El campo 'reporter' es obligatorio"}), 400
    if not description or len(description) < 10:
        return jsonify({"error": "La descripción debe tener al menos 10 caracteres"}), 400

    new_incident = Incident(
        reporter=reporter,
        description=description
    )
    db.session.add(new_incident)
    db.session.commit()

    return jsonify({
        "id": new_incident.id,
        "reporter": new_incident.reporter,
        "description": new_incident.description,
        "status": new_incident.status,
        "created_at": new_incident.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 201


# Obtener todos los incidentes
@app.route('/incidents', methods=['GET'])
def get_incidents():
    all_incidents = Incident.query.all()
    result = []
    for i in all_incidents:
        result.append({
            "id": i.id,
            "reporter": i.reporter,
            "description": i.description,
            "status": i.status,
            "created_at": i.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(result)


# Obtener un incidente específico 
@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incidente no encontrado"}), 404

    return jsonify({
        "id": incident.id,
        "reporter": incident.reporter,
        "description": incident.description,
        "status": incident.status,
        "created_at": incident.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })


# Actualizar el estado de un incidente
@app.route('/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incidente no encontrado"}), 404

    data = request.json
    new_status = data.get('status')

    if new_status not in ['pendiente', 'en proceso', 'resuelto']:
        return jsonify({"error": "Estado inválido"}), 400

    incident.status = new_status
    db.session.commit()

    return jsonify({
        "id": incident.id,
        "status": incident.status
    })


# Eliminar un incidente
@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incidente no encontrado"}), 404

    db.session.delete(incident)
    db.session.commit()

    return jsonify({"message": f"Incidente con ID {incident_id} eliminado"})

if __name__ == '__main__':
    app.run(debug=True)


