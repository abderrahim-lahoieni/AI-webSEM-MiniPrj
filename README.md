![image](https://github.com/user-attachments/assets/a967d9cf-fa68-42bb-ab5d-1120c97eb3c7)
# Base de Connaissances RDF avec Interface SPARQL

Ce projet vise à créer une base de connaissances basée sur RDF (Resource Description Framework) et à fournir une interface web pour interroger ces données à l'aide de requêtes SPARQL. Le projet permet également de visualiser les résultats sous forme de graphiques et de tableaux.

## Fonctionnalités

- **Téléversement de fichiers RDF :** Les utilisateurs peuvent téléverser des fichiers RDF (`.ttl`, `.rdf`, `.xml`) pour enrichir la base de connaissances.
- **Exécution de requêtes SPARQL :** Une interface permet d'exécuter des requêtes SPARQL sur les données RDF.
- **Affichage des résultats :** Les résultats peuvent être affichés en JSON ou sous forme de tableau HTML.
- **Mode Local et En Ligne :** Les requêtes peuvent être exécutées sur des fichiers RDF locaux ou sur un endpoint SPARQL en ligne (comme DBpedia).

## Technologies Utilisées

- **Python :** Langage de programmation principal.
- **Flask :** Framework web pour créer l'API et l'interface utilisateur.
- **RDFlib :** Bibliothèque Python pour manipuler les données RDF.
- **SPARQLWrapper :** Bibliothèque pour exécuter des requêtes SPARQL sur des endpoints en ligne.
- **Bootstrap :** Framework CSS pour l'interface utilisateur.
- **Protégé :** Outil pour créer et gérer des ontologies RDF.

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-utilisateur/votre-projet.git
   cd votre-projet
   pip install -r requirements.txt
   python app.py
