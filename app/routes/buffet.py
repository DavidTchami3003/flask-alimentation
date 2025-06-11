from flask import Blueprint,request,jsonify
from app import db,session
from app.models.buffet import Buffet
from app.models.plat import Plat

buffet_bp=Blueprint('buffet',__name__)

@buffet_bp.route('/api/buffets/generer', methods=['POST'])
def create_buffet():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    user_id=session['user_id']
    
    data = request.json
    nom = data.get('nom')
    date = data.get('date')
    lieu = data.get('lieu')
    plats_ids = data.get('plats', [])
    # Vérification que tous les champs requis sont présents
    if not all([nom, date, lieu, plats_ids]):
        return jsonify({"erreur": "Champs manquants"}), 400

    #Création du buffet
    buffet = Buffet(user_id=user_id,nom=nom, date=date, lieu=lieu)

    #Ajoute des plats au buffet
    for pid in plats_ids:
        plat = Plat.query.get(pid)
        if plat:
            buffet.plats.append(plat)

    db.session.add(buffet)
    db.session.commit()

    return jsonify({"message": "Buffet créé", "id": buffet.id})

@buffet_bp.route('/api/buffets', methods=['GET'])
def get_buffets():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    buffets = Buffet.query.all()
    result = []
    
    #Génération de la liste des buffets
    for b in buffets:
        result.append({
            "id": b.id,
            "nom": b.nom,
            "date": b.date.strftime('%Y-%m-%d %H:%M:%S'),
            "lieu": b.lieu,
            "plats": [{"id": p.id, "nom": p.nom} for p in b.plats]
        })
    return jsonify(result)

@buffet_bp.route('/api/buffets/<int:buffet_id>',methods=['GET'])
def get_buffet(buffet_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    buffet=Buffet.query.get_or_404(buffet_id)
    
    return jsonify({
        "id":buffet.id,
        "nom":buffet.nom,
        "date":buffet.date.strftime('%Y-%m-%d %H:%M:%S'),
        "lieu":buffet.lieu,
        "plats":[{"id":p.id,"nom":p.nom} for p in buffet.plats]
    })

@buffet_bp.route('/api/buffets/<int:id>', methods=['DELETE'])
def delete_buffet(id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    buffet = Buffet.query.get_or_404(id)
    db.session.delete(buffet)
    db.session.commit()
    return jsonify({"message": "Buffet supprimé"})


@buffet_bp.route('/api/buffets/<int:id>/ajouter_plats', methods=['PUT'])
def ajouter_plats_buffet(id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    buffet = Buffet.query.get_or_404(id)
    data = request.json
    plats_ids = data.get('plats', [])
    
    # Vérification que la liste des plats n'est pas vide
    if not plats_ids:
        return jsonify({"erreur": "Liste des plats vide"}), 400

    # Ajout des plats au buffet
    for pid in plats_ids:
        plat = Plat.query.get(pid)
        if plat and plat not in buffet.plats:
            buffet.plats.append(plat)

    db.session.commit()
    return jsonify({"message": "Plats ajoutés au buffet"})

@buffet_bp.route('/api/buffets/<int:id>/retirer_plats', methods=['PUT'])
def retirer_plats_buffet(id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    buffet = Buffet.query.get_or_404(id)
    data = request.json
    plats_ids = data.get('plats', [])

    # Vérification que la liste des plats n'est pas vide
    if not plats_ids:
        return jsonify({"erreur": "Liste des plats vide"}), 400

    # Retrait des plats du buffet
    for pid in plats_ids:
        plat = Plat.query.get(pid)
        # Vérification que le plat existe et est dans le buffet
        if plat and plat in buffet.plats:
            buffet.plats.remove(plat)

    db.session.commit()
    return jsonify({"message": "Plats retirés du buffet"})

@buffet_bp.route('/api/buffets', methods=['DELETE'])
def api_supprimer_tous_buffets():
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']
    buffets = Buffet.query.filter_by(user_id=user_id).all()
    
    for buffet in buffets:
        db.session.delete(buffet)
    
    db.session.commit()
    
    return jsonify({"message": "Tous les buffets ont été supprimés avec succès"})