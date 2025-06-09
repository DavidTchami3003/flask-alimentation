from app import db
from app.models.plat import Plat

class ImagePlat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plat_id = db.Column(db.Integer, db.ForeignKey('plat.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    plat = db.relationship("Plat", back_populates="images")
