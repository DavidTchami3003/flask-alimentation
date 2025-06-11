from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.Text,nullable=False)

    allergies= db.relationship('AllergieDeclaree', backref='user', lazy=True)
    consommations = db.relationship('Consommation', backref='user', lazy=True)
    buffets = db.relationship('Buffet', backref='plat', lazy=True)
    plannings = db.relationship('PlanningHebdo', backref='user', lazy=True)

    def set_password(self, password):
        """Set the password for the user."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the password for the user."""
        return check_password_hash(self.password, password)