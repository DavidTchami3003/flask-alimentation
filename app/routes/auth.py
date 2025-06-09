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
        return jsonify({"error" : "Champs manquants"}),400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Nom d'utilisateur déjà pris"})
    
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
    if user and user.check_password(password):
        session['user_id']=user.id
        return jsonify({"Message":"Connexion réussie","user_id":user.id})
    return jsonify({"error": {"Identifiants invalides"}}),401