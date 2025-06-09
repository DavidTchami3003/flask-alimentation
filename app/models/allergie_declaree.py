from app import db
import datetime

class AllergieDeclaree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plat_id = db.Column(db.Integer, db.ForeignKey('plat.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)