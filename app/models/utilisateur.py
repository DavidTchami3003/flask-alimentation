from app import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(80),nullalble=False)

    allergies= db.relationship('AllergieDeclaree', backref='user', lazy=True)
    consommations = db.relationship('Consommation', backref='user', lazy=True)
    buffets = db.relationship('Buffet', backref='plat', lazy=True)
    plannings = db.relationship('PlanningHebdomadaire', backref='plat', lazy=True)