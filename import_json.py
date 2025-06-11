import json
from sys import exit
from app import db,create_app
from app.models import Plat, User,ImagePlat

app = create_app()

def import_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    with app.app_context():
        for item in data:
            if 'username' in item and 'password' in item:
                user = User(username=item['username'])
                user.set_password(item['password'])
                db.session.add(user)
            elif 'nom' in item and 'image_folder' in item and 'ingredients' in item and item["images"]:
                plat = Plat(nom=item['nom'], image_folder=item['image_folder'], ingredients=item.get('ingredients', ''))
                db.session.add(plat)
                db.session.flush()

                for image in item['images']:
                    image_obj = ImagePlat(plat_id=plat.id, image_url=image)
                    db.session.add(image_obj)

        db.session.commit()
        print("Données importées avec succès.")

if __name__ == "__main__":
    #Ce bout de code ne doit être exécuté qu'une seule fois pour créer la base de données
    with app.app_context(): 
        plat=Plat.query.first()
        if plat is not None:
            print("La base de données n'est pas vide. Aucune importation effectuée.")
            exit(1)
    print("Importation des données...")
    import_json('app/data/plats.json')
    import_json('app/data/users.json')
    print("Importation terminée.")

# This script imports data from JSON files into the database.
# It expects two JSON files: plats.json and users.json.
# Each file should contain a list of dictionaries with the appropriate fields.
# plats.json should contain items with 'nom' and 'image_folder'.
# users.json should contain items with 'username' and 'password'.