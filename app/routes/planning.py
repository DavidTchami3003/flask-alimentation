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
    
    #Récupération de l'ID de l'utilisateur depuis la session
    user_id=session['user_id'] 
    jours=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']

    #Récupération des plats auxquels l'utilisateur présente une allergie
    plats_allergique=plats_allergiques(user_id)
    #Récupération de tous les plats auxquels il ne présente pas d'allergie
    plats_dispo=Plat.query.filter(~Plat.id.in_(plats_allergique))
    plats_dispo=list(plats_dispo)
    
    plats_disp=[]
    for i in range(4): 
        # On s'assure qu'il y a suffisamment de plats pour chaque jour de la semaine
        shuffle(plats_dispo)
        plats_disp+=plats_dispo

    #Génération du planning hebdomadaire
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

    # Récupération du planning hebdomadaire de l'utilisateur
    planning = PlanningHebdo.query.filter_by(user_id=user_id).all()

    #Renvoi des données du planning sous forme de liste de dictionnaires
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

    #Récupération du jour dont le plat est à modifier
    ligne = PlanningHebdo.query.filter_by(user_id=user_id, jour=jour.capitalize()).first()
    if not ligne:
        return jsonify({"erreur": "Jour non trouvé"}), 404

    ligne.plat_id = nouveau_plat_id
    db.session.commit()
    return jsonify({"message": f"Plat modifié pour {jour}"})

@planning_bp.route('/api/planning/<int:id>', methods=['DELETE'])
def delete_planning(id):
    if 'user_id' not in session:
        return jsonify({"erreur":"non connecté"}),401
    
    #Récupération du planning journalier par son ID
    planning = PlanningHebdo.query.get_or_404(id)
    #Suppression du planning
    db.session.delete(planning)
    db.session.commit()
    return jsonify({"message": "Planning supprimé"})


@planning_bp.route('/api/planning/', methods=['DELETE'])
def api_supprimer_tous_plannings():
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']
    # Récupération du planning hebdomadaire de l'utilisateur donc de tous ses plannings journaliers
    plannings = PlanningHebdo.query.filter_by(user_id=user_id).all()
    
    for planning in plannings:
        db.session.delete(planning)
    
    db.session.commit()
    
    return jsonify({"message": "Tous les plannings ont été supprimés avec succès"})

#Fonction pour récupérer les plats auxquels l'utilisateur présente une allergie
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
