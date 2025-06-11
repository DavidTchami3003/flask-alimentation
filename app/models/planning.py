from app import db

class PlanningHebdo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    jour=db.Column(db.String(10),nullable=False)
    plat_id=db.Column(db.Integer,db.ForeignKey('plat.id'),nullable=False)

    # utilisateur=db.relationship('User',back_popu='plannings')
    plat=db.relationship("Plat",back_populates='plannings')