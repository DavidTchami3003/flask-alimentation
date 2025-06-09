from app import db

class Plat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    ingredients=db.Column(db.Text,nullable=True)
    image_folder=db.Column(db.String(100),nullable=True)
    
    allergies = db.relationship('AllergieDeclaree', backref='plat', lazy=True)
    images = db.relationship('ImagePlat', backref='plat', lazy=True)
    consommations = db.relationship('Consommation', backref='plat', lazy=True)
    buffets = db.relationship('Buffet', backref='plat', lazy=True)
    plannings = db.relationship('PlanningHebdomadaire', backref='plat', lazy=True)