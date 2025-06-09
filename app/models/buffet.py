from app import db

class Buffet(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(100),nullable=False)
    date=db.Column(db.Date,nullable=False)
    lieu=db.Column(db.String(100),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    plats=db.relationship("Plat",secondary="buffet_plat",backref="buffets")

buffet_plat = db.Table('buffet_plat',
    db.Column('buffet_id', db.Integer, db.ForeignKey('buffet.id'), primary_key=True),
    db.Column('plat_id', db.Integer, db.ForeignKey('plat.id'), primary_key=True)
)
