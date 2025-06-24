from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime
from flask import send_from_directory

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'sensor_data.db')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_FOLDER = os.path.join(BASE_DIR, 'frontend')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor TEXT NOT NULL,
                value INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/api/pintoweb', methods=['POST'])
def receive_data():
    data = request.get_json()

    if not data or 'sensor' not in data or 'value' not in data:
        return jsonify({'error': 'Invalid request, must include sensor and value'}), 400

    sensor = data['sensor']
    value = int(data['value'])
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (sensor, value, timestamp)
            VALUES (?, ?, ?)
        ''', (sensor, value, timestamp))
        conn.commit()

    return jsonify({'status': 'success'}), 201

@app.route('/api/pintoweb/data', methods=['GET'])
def get_data():
    limit = request.args.get('limit', default=10, type=int)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sensor, value, timestamp
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()

    result = [
        {'sensor': row[0], 'value': row[1], 'timestamp': row[2]}
        for row in rows
    ]
    return jsonify(result)

#@app.route('/')
#def serve_frontend():
#    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
