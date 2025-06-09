from app import db
import datetime
class Consommation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plat_id = db.Column(db.Integer, db.ForeignKey('plat.id'), nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    a_ete_allergique = db.Column(db.Boolean, default=False)