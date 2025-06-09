from flask import Blueprint,request,jsonify,send_file
from app import db,session
from app.models.plat import Plat
from app.models.consommation import Consommation
from random import randint

plat_bp=Blueprint('plat',__name__)

@plat_bp.route('api/plats',methods=['GET'])
def get_plats():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    plats=Plat.query.all()
    return jsonify([{"id":p.id,"nom":p.nom,"ingrédients":p.ingredients} for p in plats])

@plat_bp.route('api/plats',methods=['POST'])
def create_plat():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    data=request.json
    nom=data.get('nom')
    ingredients=data.get('ingredients','')
    image_path=data.get('image_path',"")
    if not nom:
        return jsonify({"erreur":"Nom requis."}),400
    
    if Plat.query.filter_by(nom=nom).first():
        return jsonify({"erreur":"Nom de plat déjà existant"})
    
    nouveau_plat=Plat(nom=nom,ingredients=ingredients, image_folder=image_path)
    db.session.add(nouveau_plat)
    db.session.commit()
    return jsonify({"id":nouveau_plat.id,"nom":nouveau_plat.nom}),201

@plat_bp.route('api/plats/<int:plat_id>',methods=['GET'])
def get_plat(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    plat=Plat.query.get_or_404(plat_id)
    return jsonify({"id":plat.id,"nom":plat.nom,"ingredients":plat.ingredients})

@plat_bp.route('/api/plats/<int:plat_id>/image',methods=['GET'])
def get_plat_image(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    r=randint(1,15)
    plat=Plat.query.get_or_404(plat_id)
    image_path = f"static/images/{plat.image_folder}/{r}.jpeg"
    if not image_path:
        return jsonify({"erreur":"Image non trouvée"}),404
    return send_file(image_path, mimetype='image/jpeg')

@plat_bp.route('/api/plats/<int:plat_id>',methods=['PUT'])
def update_plat(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    plat=Plat.query.get_or_404(plat_id)
    data=request.json
    nom=data['nom']
    if not nom:
        return jsonify({"erreur":"Nom requis."}),400
    plat.nom=nom
    db.session.commit()
    return jsonify({"message":"Plat mis à jour","id":plat.id,"nom":plat.nom})

@plat_bp.route('/api/plats/<int:plat_id>',methods=['DELETE'])
def delete_plat(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    plat=Plat.query.get_or_404(plat_id)
    db.session.delete(plat)
    db.session.commit()
    return jsonify({"message":"Plat supprimé avec succès"})

@plat_bp.route('/api/plats/plats_allergiques',methods=['GET'])
def get_plats_allergiques(utilisateur_id=session['user_id']):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    allergenes = []
    plats = Plat.query.all()
    for plat in plats:
        conso = Consommation.query.filter_by(utilisateur_id=utilisateur_id, plat_id=plat.id).all()
        if not conso:
            continue
        total = len(conso)
        allergie_count = sum([1 for c in conso if c.a_ete_allergique])
        if total > 4 and allergie_count / total > 0.3:
            allergenes.append(plat.id)
    return jsonify({"plats":allergenes})

