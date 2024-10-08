import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.doctissimo.fr/asp/medicaments/les-medicaments-les-plus-prescrits.htm'
response = requests.get(url)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')

post_content = soup.find('div', {'class':'search-results'})
children = post_content.find_all('li')

# Dictionnaire pour stocker les médicaments
medicament_dict = {"medicament": []}

for child in children:
    text = child.get_text(strip=True)
    # Extraire le nom du médicament après le numéro
    if '. ' in text:
        name = text.split('. ')[1]
        medicament_dict["medicament"].append(name)

# Convertir le dictionnaire en chaîne JSON
json_data = json.dumps(medicament_dict, indent=4, ensure_ascii=False)

# Écrire les données JSON dans un fichier
with open('medicaments.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
print(json_data)
print("Les données ont été enregistrées dans le fichier medicaments.json avec succès.")
print(medicament_dict)
import sqlite3
conn = sqlite3.connect('medicaments.db')
cursor = conn.cursor()

# Supprimer la table si elle existe déjà pour éviter les conflits
cursor.execute('DROP TABLE IF EXISTS medicament')

# Créer la table 'medicaments' avec une clé primaire 'Id' et une clé secondaire 'prescrits'
cursor.execute('''
CREATE TABLE medicament (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescrits TEXT NOT NULL
)
''')

# Insérer les médicaments dans la table
for name in medicament_dict["medicament"]:
    cursor.execute('''
    INSERT INTO medicament (prescrits)
    VALUES (?)
    ''', (name,))

# Valider les changements
conn.commit()

# Étape 3 : Afficher le schéma de la table
cursor.execute("PRAGMA table_info(medicament)")
schema = cursor.fetchall()

print("\nSchéma de la table 'medicament':")
for column in schema:
    print(column)

# Étape 4 : Afficher les données de la table
cursor.execute("SELECT * FROM medicament")
rows = cursor.fetchall()

print("\nDonnées de la table 'medicament':")
for row in rows:
    print(row)

# Fermer la connexion
conn.close()
print("Les données ont été insérées dans la base de données avec succès.")

