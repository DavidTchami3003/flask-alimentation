from app import create_app,db

app=create_app()
with app.app_context():
    # Création des tables
    db.create_all()
    print("Base de données initialisée avec succès.")