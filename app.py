from flask import Flask, request, jsonify, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef
import os

# Initialiser l'application Flask
app = Flask(__name__)

# Dossier pour stocker les fichiers RDF téléchargés
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Endpoint SPARQL en ligne (exemple : DBpedia)
SPARQL_ENDPOINT = "https://dbpedia.org/sparql"

# Charger la base de connaissances RDF par défaut (optionnel)
graph = Graph()
graph.parse("data/knowledge_base.ttl", format="turtle")

# Fonction pour extraire le nom de la ville à partir de l'URI
def extract_city_name(uri):
    return uri.split("/")[-1]

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour télécharger un fichier RDF
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200

# Route pour exécuter les requêtes SPARQL
@app.route('/sparql', methods=['POST'])
def sparql_query():
    # Récupérer la requête SPARQL depuis le corps de la requête
    query = request.json.get('query')
    filename = request.json.get('filename')  # Nom du fichier RDF à utiliser
    use_online_endpoint = request.json.get('use_online_endpoint', False)  # Utiliser l'endpoint en ligne

    if not query:
        return jsonify({"error": "No query provided"}), 400

    if use_online_endpoint:
        # Exécuter la requête SPARQL sur l'endpoint en ligne
        try:
            sparql = SPARQLWrapper(SPARQL_ENDPOINT)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Charger le fichier RDF spécifié (ou utiliser le fichier par défaut)
        if filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            graph = Graph()
            graph.parse(filepath, format="turtle")
        else:
            # Utiliser le fichier RDF par défaut
            graph = Graph()
            graph.parse("data/knowledge_base.ttl", format="turtle")

        # Exécuter la requête SPARQL
        try:
            results = graph.query(query)
            # Formater les résultats pour l'affichage
            output = []
            for row in results:
                formatted_row = {}
                for var in results.vars:
                    value = row[var]
                    if value:
                        if isinstance(value, URIRef) and "city" in str(var).lower():
                            # Extraire le nom de la ville si la variable est une URI et contient "city"
                            formatted_row[str(var)] = {
                                "type": "literal",
                                "value": extract_city_name(str(value))  # Extraire le nom de la ville
                            }
                        else:
                            formatted_row[str(var)] = {
                                "type": "uri" if isinstance(value, URIRef) else "literal",
                                "value": str(value)
                            }
                    else:
                        formatted_row[str(var)] = {"type": "literal", "value": "N/A"}
                output.append(formatted_row)
            return jsonify({"head": {"vars": list(results.vars)}, "results": {"bindings": output}})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)