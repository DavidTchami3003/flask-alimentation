from flask import Blueprint,request,jsonify
from app import db,session
from app.models.buffet import Buffet
from app.models.plat import Plat

buffet_bp=Blueprint('buffet',__name__)

@buffet_bp.route('/api/buffets', methods=['POST'])
def create_buffet():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    data = request.json
    nom = data.get('nom')
    date = data.get('date')
    lieu = data.get('lieu')
    plats_ids = data.get('plats', [])

    if not all([nom, date, lieu]):
        return jsonify({"error": "Champs manquants"}), 400

    buffet = Buffet(nom=nom, date=date, lieu=lieu)

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
    for b in buffets:
        result.append({
            "id": b.id,
            "nom": b.nom,
            "date": b.date.strftime('%Y-%m-%d %H:%M:%S'),
            "lieu": b.lieu,
            "plats": [{"id": p.id, "nom": p.nom} for p in b.plats]
        })
    return jsonify(result)

@buffet_bp.route('/api/buffet/<int:buffet_id>',methods=['GET'])
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

    for pid in plats_ids:
        plat = Plat.query.get(pid)
        if plat and plat in buffet.plats:
            buffet.plats.remove(plat)

    db.session.commit()
    return jsonify({"message": "Plats retirés du buffet"})
