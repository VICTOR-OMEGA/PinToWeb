from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String(50))
    value = db.Column(db.Integer)
    timestamp = db.Column(db.String(100))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/terraflow', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data or 'sensor' not in data or 'value' not in data or 'timestamp' not in data:
        return jsonify({"error": "Invalid payload"}), 400

    entry = SensorData(sensor=data['sensor'], value=data['value'], timestamp=data['timestamp'])
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Data stored"}), 201

@app.route('/api/terraflow/data', methods=['GET'])
def get_data():
    limit = int(request.args.get('limit', 10))
    rows = SensorData.query.order_by(SensorData.id.desc()).limit(limit).all()
    return jsonify([{
        "sensor": r.sensor,
        "value": r.value,
        "timestamp": r.timestamp
    } for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

