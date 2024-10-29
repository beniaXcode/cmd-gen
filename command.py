from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commands.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template = db.Column(db.String(500))
    generated_command = db.Column(db.String(500))



@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/get_commands', methods=['GET'])
def get_commands():
    commands = Command.query.all()
    return jsonify([{'id': cmd.id, 'template': cmd.template, 'generated_command': cmd.generated_command} for cmd in commands])

@app.route('/save_command', methods=['POST'])
def save_command():
    data = request.json
    new_command = Command(template=data['template'], generated_command=data['generated_command'])
    db.session.add(new_command)
    db.session.commit()
    return jsonify({'status': 'Command saved'})

@app.route('/edit_command', methods=['POST'])
def edit_command():
    data = request.json
    command = Command.query.get(data['id'])
    command.template = data['template']
    command.generated_command = data['generated_command']
    db.session.commit()
    return jsonify({'status': 'Command updated'})

@app.route('/delete_command', methods=['POST'])
def delete_command():
    data = request.json
    command = Command.query.get(data['id'])
    db.session.delete(command)
    db.session.commit()
    return jsonify({'status': 'Command deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
