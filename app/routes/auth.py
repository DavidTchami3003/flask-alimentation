from flask import Blueprint, request,jsonify
from app import db,session
from app.models.utilisateur import User

auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/api/register',methods=['POST'])
def api_register():
    data=request.json
    username=data.get("username")
    password=data['password']

    if not username or not password :
        return jsonify({"erreur" : "Champs manquants"}),400
    
    # Vérification de la présence du nom d'utilisateur dans la base de données
    if User.query.filter_by(username=username).first():
        return jsonify({"erreur": "Nom d'utilisateur déjà pris"})
    
    new_user=User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id']=new_user.id
    return jsonify({"message": "Inscription réussie","user_id":new_user.id}),2

@auth_bp.route('/api/login',methods=['POST'])
def api_login():
    data=request.json
    username=data.get('username')
    password=data['password']

    if not username or not password:
        return jsonify({'erreur':'champs manquants'})

    user=User.query.filter_by(username=username).first()
    # Vérification de l'existence de l'utilisateur et de la validité du mot de passe
    if user and user.check_password(password):
        session['user_id']=user.id
        return jsonify({"Message":"Connexion réussie","user_id":user.id}),200
    return jsonify({"erreur": "Identifiants invalides"}),401

@auth_bp.route('/api/logout',methods=['POST'])
def logout():
    #Suppression de la clé et de l'id de l'utilisateur de la session
    session.pop('user_id',None) 

    return jsonify({"message": "Déconnexion réussie"}), 200

@auth_bp.route('/api/users', methods=['GET'])
def get_users():
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    #Récupération des informations de l'utilisateur connecté actuellement
    user_admin=User.query.get_or_404(session['user_id']) 

    #Seul l'administrateur peut accéder à cette route
    if user_admin.check_password('davido') and user_admin.name=='David': 
        # Récupérer tous les utilisateurs
        users = User.query.all()
        if not users:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        
        return jsonify([{"id": user.id, "username": user.username,"password":user.password} for user in users]), 200
    else:
        return jsonify({"erreur":"Vous n'avez pas les droits pour accéder à cette ressource"})
    
@auth_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    user = User.query.get_or_404(user_id)
    user_admin= User.query.get_or_404(session['user_id'])
    
    # Seul l'administrateur peut accéder à cette route
    if user_admin.check_password('davido') and user_admin.name=='David': 
        # Récupérer l'utilisateur par ID
        return jsonify({"id": user.id, "username": user.username,"password":user.password}), 200
    else:
        return jsonify({"erreur":"Vous n'avez pas les droits pour accéder à cette ressource"}), 403
    
@auth_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    user = User.query.get_or_404(user_id)
    user_admin = User.query.get_or_404(session['user_id']) 

    # Seul l'administrateur peut supprimer un utilisateur
    if user_admin.check_password('davido') and user_admin.name=='David': 
        # Supprimer l'utilisateur
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Utilisateur supprimé avec succès"}), 200
    else:
        return jsonify({"erreur":"Vous n'avez pas les droits pour accéder à cette ressource"}), 403

@auth_bp.route('/api/users', methods=['PUT'])
def update_user():
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    user_id=session['user_id']
    #Récupération de l'utilisateur connecté
    user = User.query.get_or_404(user_id)

    data = request.json
    new_username = data.get('username')
    new_password = data.get('password')

    if new_username:
        user.username = new_username
    if new_password:
        user.set_password(new_password)

    db.session.commit()
    return jsonify({"message": "Utilisateur mis à jour avec succès"}), 200