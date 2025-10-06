from flask import Flask, request, jsonify, render_template
import heapq

app = Flask(__name__)

# ------------------ Classes ------------------
class Patient:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority  # lower = higher priority

class Hospital:
    def __init__(self):
        self.queue = []

    def add_patient(self, name, priority):
        patient = Patient(name, priority)
        heapq.heappush(self.queue, patient)

    def treat_patient(self):
        if not self.queue:
            return None
        return heapq.heappop(self.queue)

    def get_waiting_list(self):
        return sorted(self.queue, key=lambda x: x.priority)

hospital = Hospital()

# ------------------ Routes ------------------
@app.route('/')
def home():
    return render_template('index.html')  # loads your HTML UI

@app.route('/add', methods=['POST'])
def add_patient():
    data = request.get_json()
    name = data.get('name', '').strip()
    priority = data.get('priority')

    if not name:
        return jsonify({'error': 'Name is required!'}), 400
    if priority not in [1, 2, 3]:
        return jsonify({'error': 'Priority must be 1, 2, or 3'}), 400

    hospital.add_patient(name, priority)
    return jsonify({'message': f'Patient {name} added with priority {priority}'}), 200

@app.route('/treat', methods=['POST'])
def treat_patient():
    patient = hospital.treat_patient()
    if not patient:
        return jsonify({'message': 'No patients waiting!'}), 200
    return jsonify({'message': f'Treating {patient.name} (Priority {patient.priority})'}), 200

@app.route('/list', methods=['GET'])
def waiting_list():
    patients = hospital.get_waiting_list()
    result = [{'name': p.name, 'priority': p.priority} for p in patients]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
