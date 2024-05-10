from flask import Flask, jsonify, request
from pymongo import MongoClient
import config as c
app = Flask(__name__)

# MongoDB Connection
client = MongoClient(c.db_url)
db = client[c.db_name]  # Change 'my_database' to your database name


# Route to list all databases
@app.route('/databases', methods=['GET'])
def list_databases():
    databases = client.list_database_names()
    return jsonify(databases)


# Route to list all collections in a database
@app.route('/collections/<database_name>', methods=['GET'])
def list_collections(database_name):
    collections = client[database_name].list_collection_names()
    return jsonify(collections)


# Route to insert a document into a collection
@app.route('/collections/<database_name>/<collection_name>', methods=['POST'])
def insert_document(database_name, collection_name):
    collection = client[database_name][collection_name]
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'inserted_id': str(result.inserted_id)})


# Route to retrieve all documents from a collection
@app.route('/collections/<database_name>/<collection_name>', methods=['GET'])
def get_documents(database_name, collection_name):
    collection = client[database_name][collection_name]
    documents = list(collection.find())
    return jsonify(documents)


# Route to retrieve a specific document from a collection
@app.route('/collections/<database_name>/<collection_name>/<document_id>', methods=['GET'])
def get_document(database_name, collection_name, document_id):
    collection = client[database_name][collection_name]
    document = collection.find_one({'_id': document_id})
    return jsonify(document)


if __name__ == '__main__':
    app.run(debug=True)
