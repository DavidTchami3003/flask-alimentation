from flask import Blueprint,jsonify,request
from random import shuffle
from app import db,session
from app.models.planning import PlanningHebdo
from app.models.utilisateur import User
from app.models.plat import Plat
from app.models.consommation import Consommation

planning_bp=Blueprint('planning',__name__)

@planning_bp.route('/api/planning/generer',methods=['POST'])
def generer_planning():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    user_id=session['user_id']
    jours=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
    utilisateur=User.query.get_or_404(user_id)

    plats_allergique=plats_allergiques(session['user_id'])
    plats_dispo=Plat.query.filter(~Plat.id.in_(plats_allergique))
    
    plats_disp=[]
    for i in range(2):
        shuffle(plats_dispo)
        plats_disp+=plats_dispo

    for i,jour in enumerate(jours):
        plan=PlanningHebdo(user_id=user_id,jour=jour,plat_id=plats_disp[i].id)
        db.session.add(plan)

    db.session.commit()
    return jsonify({"message":"Planning hebdomadaire généré"})

@planning_bp.route('/api/planning', methods=['GET'])
def voir_planning():
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    user_id=session["user_id"]
    planning = PlanningHebdo.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"jour": p.jour, "plat": p.plat.nom}
        for p in planning
    ])

@planning_bp.route('/api/planning/<jour>', methods=['PUT'])
def modifier_jour_planning(jour):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    user_id=session['user_id']
    data = request.json
    nouveau_plat_id = data.get("plat_id")

    ligne = PlanningHebdo.query.filter_by(user_id=user_id, jour=jour.capitalize()).first()
    if not ligne:
        return jsonify({"erreur": "Jour non trouvé"}), 404

    ligne.plat_id = nouveau_plat_id
    db.session.commit()
    return jsonify({"message": f"Plat modifié pour {jour}"})



def plats_allergiques(utilisateur_id):
    allergenes = []
    plats = Plat.query.all()
    for plat in plats:
        conso = Consommation.query.filter_by(user_id=utilisateur_id, plat_id=plat.id).all()
        if not conso:
            continue
        total = len(conso)
        allergie_count = sum([1 for c in conso if c.a_rapporte_allergie])
        if total > 4 and allergie_count / total > 0.3:
            allergenes.append(plat.id)
    return allergenes
