from flask import Blueprint,request,jsonify
from app import db,session
from app.models.consommation import Consommation
from app.models.utilisateur import User
from app.models.plat import Plat

conso_bp=Blueprint('conso',__name__)

@conso_bp.route('/api/manger',methods=['POST'])
def api_manger():
    if 'user_id' not in session:
        return jsonify({"error":"Non connecté"})
    
    data=request.json
    plat_id=data.get('plat_id')
    allergique=data.get('allergique',False)

    user=User.query.get(session['user_id'])
    
    #Récupération de toutes les consommations de l'utilisateur pour ce plat
    consommations=Consommation.query.filter_by(user_id=user.id,plat_id=plat_id).all() 
    #Vérification s'il y a des consommations précédentes où l'utilisateur a signalé une allergie
    allergies_precedentes=[c for c in consommations if c.a_ete_allergique] 

    plat=Plat.query.get_or_404(plat_id)
    #Création d'une nouvelle consommation
    consommation=Consommation(              
        user_id=session['user_id'],
        plat_id=plat.id,
        a_ete_allergique=allergique
    )
    db.session.add(consommation)
    db.session.commit()
    return jsonify({"Attention":"Vous avez déjà signaler une allergie à ce plat","message":"Bon appétit"} if allergies_precedentes else {"message":"Bon appétit !"})


@conso_bp.route('/api/statut/<int:plat_id>',methods=['GET'])
def api_statut_allergique (plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']

    #Nombre total de consommations pour ce plat par l'utilisateur
    total=Consommation.query.filter_by(user_id=user_id,plat_id=plat_id).count() 
    #Nombre de fois où l'utilisateur a signalé une allergie pour ce plat
    nb_allergies=Consommation.query.filter_by(user_id=user_id,plat_id=plat_id,a_ete_allergique=True).count() 

    statut=None
    if total>0:
        ratio=nb_allergies/total
        #Si l'utilisateur a signalé une allergie plus de 30% du temps et qu'il a consommé le plat plus de 4 fois, il est considéré comme allergique
        statut=True if ratio>0.3 and total >4 else False 
    
    return jsonify({
        "total":total,
        "allergies":nb_allergies,
        'allergique_officiel':statut
    })

@conso_bp.route('/api/consommations', methods=['GET'])
def api_consommations():
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']

    #Récupération de toutes les consommations de l'utilisateur
    consommations = Consommation.query.filter_by(user_id=user_id).all() 
    
    result = []
    for conso in consommations:
        #Récupération du plat associé à la consommation
        plat = Plat.query.get(conso.plat_id) 
        #Création d'une liste de dictionnaires avec les informations de chaque consommation
        result.append({   
            "plat_id": conso.plat_id,
            "plat_nom": plat.nom if plat else "Inconnu",
            "a_ete_allergique": True if conso.a_ete_allergique else False
        })
    
    return jsonify(result)

@conso_bp.route('/api/consommations/<int:plat_id>', methods=['GET'])
def api_consommation_par_plat(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']

    #Récupération de toutes les consommations de l'utilisateur pour ce plat
    consommations = Consommation.query.filter_by(user_id=user_id, plat_id=plat_id).all() 
    
    result = []
    for conso in consommations:
        result.append({
            "plat_id": conso.plat_id,
            "a_ete_allergique": True if conso.a_ete_allergique else False,
            "date":conso.date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(result)

@conso_bp.route('/api/consommations/<int:plat_id>', methods=['DELETE'])
def api_supprimer_consommation(plat_id):
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']
    #Récupération de la consommation de l'utilisateur pour ce plat
    consommation = Consommation.query.filter_by(user_id=user_id, plat_id=plat_id).first() 
    
    if not consommation:
        return jsonify({"message": "Consommation non trouvée"}),404
    
    db.session.delete(consommation) #Suppression de la consommation
    db.session.commit()
    
    return jsonify({"message": "Consommation supprimée avec succès"})

@conso_bp.route('/api/consommations', methods=['DELETE'])
def api_supprimer_toutes_consommations():
    if 'user_id' not in session:
        return jsonify({"erreur":"Non connecté"}),401
    
    user_id=session['user_id']
    consommations = Consommation.query.filter_by(user_id=user_id).all() #Récupération de toutes les consommations de l'utilisateur
    
    if not consommations:
        return jsonify({"message": "Aucune consommation à supprimer"}), 404
    
    # Suppression de toutes les consommations de l'utilisateur
    for conso in consommations:
        db.session.delete(conso)
    
    db.session.commit()
    
    return jsonify({"message": "Toutes les consommations ont été supprimées avec succès"})
