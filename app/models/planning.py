from app import db

class PlanningHebdo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    jour=db.Column(db.String(10),nullable=False)
    plat_id=db.Column(db.Integer,db.ForeignKey('plat.id'),nullable=False)

    utilisateur=db.relationship('User',backref='plannings')
    plat=db.relationship("Plat")