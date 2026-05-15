from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'requests.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            project_title TEXT NOT NULL,
            problem_description TEXT NOT NULL,
            urgency TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    
    if not all([data.get('name'), data.get('email'), data.get('department'), 
                data.get('project_title'), data.get('problem_description'), data.get('urgency')]):
        return jsonify({'error': 'All fields are required'}), 400
    
    request_id = 'REQ-' + str(uuid.uuid4())[:6].upper()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db()
    conn.execute('''
        INSERT INTO requests (id, name, email, department, project_title, problem_description, urgency, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
    ''', (request_id, data['name'], data['email'], data['department'], 
          data['project_title'], data['problem_description'], data['urgency'], created_at))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Request submitted successfully', 'id': request_id}), 201
@app.route('/api/requests', methods=['GET'])
def get_requests():
    department = request.args.get('department')
    status = request.args.get('status')
    
    conn = get_db()
    query = 'SELECT * FROM requests WHERE 1=1'
    params = []
    
    if department:
        query += ' AND department = ?'
        params.append(department)
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    query += ' ORDER BY created_at DESC'
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route('/api/requests/<request_id>', methods=['GET'])
def get_request(request_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM requests WHERE id = ?', (request_id,)).fetchone()
    conn.close()
    
    if row is None:
        return jsonify({'error': 'Request not found'}), 404
    
    return jsonify(dict(row))

@app.route('/api/requests/<request_id>/status', methods=['PUT'])
def update_status(request_id):
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['Pending', 'Reviewing', 'Approved', 'Rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    conn = get_db()
    conn.execute('UPDATE requests SET status = ? WHERE id = ?', (new_status, request_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Status updated successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    
    total = conn.execute('SELECT COUNT(*) as count FROM requests').fetchone()['count']
    
    status_rows = conn.execute('SELECT status, COUNT(*) as count FROM requests GROUP BY status').fetchall()
    
    dept_rows = conn.execute('SELECT department, COUNT(*) as count FROM requests GROUP BY department').fetchall()
    
    conn.close()
    
    return jsonify({
        'total': total,
        'by_status': {row['status']: row['count'] for row in status_rows},
        'by_department': {row['department']: row['count'] for row in dept_rows}
    })

if __name__ == '__main__':
    app.run(debug=True)