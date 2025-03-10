from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Room {self.nombre}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
    
class HouseKeeper(db.Model):
    __tablename__ = 'housekeeper'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<HouseKeeper {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
    
class HouseKeeperTask(db.Model):
    __tablename__ = 'housekeepertask'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(120), unique=True, nullable=False)
    condition = db.Column(db.String(80), unique=False, nullable=False)
    assignment_date = db.Column(db.String(80), unique=False, nullable=False)
    submission_date = db.Column(db.String(80), unique=False, nullable=False)
    id_room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)
    id_housekeeper = db.Column(db.Integer, db.ForeignKey('housekeeper.id'), nullable=True)

    room = db.relationship('Room', backref='housekeepertask')
    housekeeper = db.relationship('HouseKeeper', backref='housekeepertask')

    def __repr__(self):
        return f'<HouseKeeperTask {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "photo": self.photo,
            "condition": self.condition,
            "assignment_date": self.assignment_date,
            "submission_date": self.submission_date,
            "id_room": self.id_room,
            "id_housekeeper": self.id_housekeeper,
        }