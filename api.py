from flask import Flask, jsonify, request, json, make_response
from flask_sqlalchemy import SQLAlchemy

#Init Flask app and SQLAlechmy/SQLite Database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sensor.db"
db = SQLAlchemy(app)

#SQLite database model instantiated with SQLAlchemy
class PeopleCounters(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sensor = db.Column(db.Text, nullable = False)
    ts = db.Column(db.Text, nullable = False)
    into = db.Column(db.Integer, nullable = False)
    out = db.Column(db.Integer, nullable = False)

    def __str__(self):
        return f'{self.id} {self.sensor} {self.ts} {self.into} {self.out}'

#Function that serialize data for jsonify
def counters_serializer(counters):
    return{
        'id': counters.id,
        'sensor': counters.sensor,
        'ts': counters.ts,
        'into': counters.into,
        'out': counters.out
    }

#GET /api endpoint returning all sensor entries
@app.route('/api', methods=['GET'])
def index():
    return make_response(jsonify([*map(counters_serializer, PeopleCounters.query.all())]), 200)

#POST /api/webhook endpoint adding a new sensor entry in the database
@app.route('/api/webhook', methods=['POST'])
def add():
    request_data = json.loads(request.data)
    counter = PeopleCounters(sensor=request_data['sensor'], ts=request_data['time'], into=request_data['into'], out=request_data['out'])
    db.session.add(counter)
    db.session.commit()
    return make_response(jsonify(counters_serializer(counter)), 201)


#GET /api/occupany? endpoint getting sensor & atInstant arguments and return number of people inside the room monitorised by "sensor" at the moment "atInstant"
@app.route('/api/occupancy', methods=['GET'])
def occupancy():
    peopleIn = 0
    peopleOut = 0
    sensor = request.args.get('sensor')
    atInstant = request.args.get('atInstant')
    for row in PeopleCounters.query.filter(PeopleCounters.sensor==sensor, PeopleCounters.ts<=atInstant):
        peopleIn += row.into
        peopleOut += row.out
    if(peopleIn==0 and peopleOut==0):
        return make_response({'inside': False}, 200)
    else:
        return make_response({'inside': peopleIn-peopleOut}, 200)

if __name__ == '__main__':
    app.run(debug=True)