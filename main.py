from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/add', methods=['POST'])
def add_contact():
    data = request.json
    contact = Contact(name=data['name'], phone=data['phone'])
    db.session.add(contact)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Контакт не найден'}), 404


@app.route('/update/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)
    if contact:
        data = request.json
        contact.name = data['name']
        contact.phone = data['phone']
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Контакт не найден'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)