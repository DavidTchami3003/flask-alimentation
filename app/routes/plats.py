from flask import Blueprint,request,jsonify,send_file
from app import db,session
from app.models.plat import Plat
from app.models.consommation import Consommation
from app.models import ImagePlat
from app.models.allergie_declaree import AllergieDeclaree
from random import randint

plat_bp=Blueprint('plat',__name__)

@plat_bp.route('/api/plats',methods=['GET'])
def get_plats():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    #Récupération de tous les plats disponibles dans la base de données
    plats=Plat.query.all()
    if not plats:
        return jsonify({"message":"Aucun plat disponible"}),404
    #Renvoi des données des plats sous forme de liste de dictionnaires
    return jsonify([{"id":p.id,"nom":p.nom,"ingrédients":p.ingredients} for p in plats])

@plat_bp.route('/api/plats',methods=['POST'])
def create_plat():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    data=request.json
    nom=data.get('nom')
    ingredients=data.get('ingredients','')
    image_path=data.get('image_path',"")

    if not nom:
        return jsonify({"erreur":"Nom requis."}),400
    
    #Vérification de la présence du nom du plat dans la base de données
    if Plat.query.filter_by(nom=nom.capitalize()).first():
        return jsonify({"erreur":"Nom de plat déjà existant"})
    
    #Creation d'un nouveau plat
    nouveau_plat=Plat(nom=nom,ingredients=ingredients, image_folder=image_path)
    db.session.add(nouveau_plat)
    db.session.commit()
    return jsonify({"id":nouveau_plat.id,"nom":nouveau_plat.nom}),201

@plat_bp.route('/api/plats/<int:plat_id>',methods=['GET'])
def get_plat(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    #Récupération du plat par son ID
    plat=Plat.query.get_or_404(plat_id)
    if not plat:    
        return jsonify({"erreur":"Plat non trouvé"}),404
    
    return jsonify({"id":plat.id,"nom":plat.nom,"ingredients":plat.ingredients})

@plat_bp.route('/api/plats/<int:plat_id>/image',methods=['GET'])
def get_plat_image(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    #Choix aléatoire d'un nombre entre 1 et 15
    r=randint(1,15)
    #Récupération du plat par son ID
    plat=Plat.query.get_or_404(plat_id)
    # Récupération des images associées à ce plat
    images=ImagePlat.query.filter_by(plat_id=plat.id).all()
    #Récupération de l'image d'identifiant r
    image=images[r-1]
    #Génération du chemin de l'image
    image_path = f"static/images/{plat.image_folder}/{image.image_url}"

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
    ingredients=data.get('ingredients','')
    image_path=data.get('image_path',"")
    
    if not ingredients:
        ingredients=plat.ingredients
    if not image_path:
        image_path=plat.image_folder
    if not nom:
        return jsonify({"erreur":"Nom requis."}),400
    
    #Mise à jour des informations du plat
    plat.nom=nom
    plat.ingredients=ingredients
    plat.image_folder=image_path
    db.session.commit()
    return jsonify({"message":"Plat mis à jour","id":plat.id,"nom":plat.nom,"ingrédients":plat.ingredients,"image_folder":plat.image_folder}),200

@plat_bp.route('/api/plats/<int:plat_id>',methods=['DELETE'])
def delete_plat(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    plat=Plat.query.get_or_404(plat_id)
    if not plat:
        return jsonify({"erreur":"Plat non trouvé"}),404
    #Suppression du plat de la base de données
    db.session.delete(plat)
    db.session.commit()
    return jsonify({"message":"Plat supprimé avec succès"})

@plat_bp.route('/api/plats/plats_allergiques',methods=['GET'])
def get_plats_allergiques():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    utilisateur_id=session['user_id']
    allergenes = []
    plats = Plat.query.all()
    
    for plat in plats:
        # Récupération de toutes les consommations de l'utilisateur pour ce plat
        conso = Consommation.query.filter_by(user_id=utilisateur_id, plat_id=plat.id).all()
        if not conso:
            continue
        
        total = len(conso)
        # Calcul du nombre de consommations où l'utilisateur a été allergique
        allergie_count = sum([1 for c in conso if c.a_ete_allergique])
        
        if total > 4 and allergie_count / total > 0.3:
            #Enregistrement de l'ID du plat allergène dans la liste
            allergenes.append(plat.id)
            # Enregistrement du plat allergène déclarés dans la base de données
            allergene=AllergieDeclaree(user_id=utilisateur_id, plat_id=plat.id)
            db.session.add(allergene)
    
    db.session.commit()

    if not allergenes:
        return jsonify({"message":"Aucun plat allergène trouvé"}),404
    return jsonify({"plats":allergenes})

