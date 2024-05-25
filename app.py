from flask import Flask, jsonify, request, render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import config as c
app = Flask(__name__)

# MongoDB Connection
client = MongoClient(c.db_url)
db = client[c.db_name]  # Change 'my_database' to your database name

# Route to list all databases
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route to list all databases
# route database
@app.route('/databases', methods=['GET'])
def list_databases():
    databases = client.list_database_names()
    databases_with_stats = []
    for database_name in databases:
        db = client[database_name]
        stats = db.command("dbstats")
        databases_with_stats.append({
            'name': database_name,
            'collections_count': len(db.list_collection_names()),
            'data_size': stats.get('dataSize', 0),
            'storage_size': stats.get('storageSize', 0),
            'index_size': stats.get('indexSize', 0),
            'file_size': stats.get('fileSize', 0)  # Use .get() to provide a default value
        })
    return render_template('databases.html', databases=databases_with_stats)

@app.route('/collections/<database_name>', methods=['GET'])
def list_collections(database_name):
    db = client[database_name]
    collections = db.list_collection_names()
    collections_with_stats = []
    for collection_name in collections:
        stats = db.command("collstats", collection_name)
        collections_with_stats.append({
            'name': collection_name,
            'document_count': stats.get('count', 0),
            'data_size': stats.get('size', 0),
            'storage_size': stats.get('storageSize', 0),
            'index_size': stats.get('totalIndexSize', 0),
            'avg_doc_size': stats.get('avgObjSize', 0)
        })
    return render_template('collections.html', collections=collections_with_stats, database=database_name)

# Route to retrieve all documents from a collection
# @app.route('/collections/<database_name>/<collection_name>', methods=['GET'])
# def get_documents(database_name, collection_name):
#     collection = client[database_name][collection_name]
#     documents = list(collection.find())
#     return render_template('documents.html', collection_name=collection_name, documents=documents)

@app.route('/collections/<database_name>/<collection_name>', methods=['GET'])
def get_documents(database_name, collection_name):
    collection = client[database_name][collection_name]
    documents = list(collection.find())
    print(f"Database: {database_name}, Collection: {collection_name}")  # Debug print
    return render_template('documents.html', collection_name=collection_name, documents=documents, database=database_name)


# Route to save a new row
@app.route('/save_new_row', methods=['POST'])
def save_new_row():
    try:
        data = request.get_json()
        # data = request.json
        app.logger.debug(f"Received data: {data}")

        database_name = data.pop('database_name')
        collection_name = data.pop('collection_name')
        collection = client[database_name][collection_name]

        new_document = {key.replace('field_', ''): value for key, value in data.items()}
        app.logger.debug(f"Inserting document: {new_document}")

        collection.insert_one(new_document)
        return jsonify(success=True)
    except Exception as e:
        app.logger.error(f"Error saving new row: {e}")
        return jsonify(success=False, error=str(e)), 500

# Route to delete a row
@app.route('/delete_row', methods=['POST'])
def delete_row():
    try:
        data = request.get_json()
        # data = request.json
        database_name = data['database_name']
        collection_name = data['collection_name']
        document_id = data['document_id']
        
        collection = client[database_name][collection_name]
        collection.delete_one({'_id': ObjectId(document_id)})
        
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500




if __name__ == '__main__':
    app.run(debug=True)