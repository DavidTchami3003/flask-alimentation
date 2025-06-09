import json
from app import db,create_app
from app.models import Plat, User

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
            elif 'nom' in item and 'image_folder' and 'ingredients' in item:
                plat = Plat(nom=item['nom'], image_folder=item['image_foler'], ingredients=item.get('ingredients', ''))
                db.session.add(plat)

        db.session.commit()
        print("Données importées avec succès.")

if __name__ == "__main__":
    import_json('plats.json')
    import_json('users.json')
    print("Importation terminée.")

# This script imports data from JSON files into the database.
# It expects two JSON files: plats.json and users.json.
# Each file should contain a list of dictionaries with the appropriate fields.
# plats.json should contain items with 'nom' and 'image_folder'.
# users.json should contain items with 'username' and 'password'.