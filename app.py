from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
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
@app.route('/databases', methods=['GET'])
def list_databases():
    databases = client.list_database_names()
    return render_template('databases.html', databases=databases)


# Route to list collections in a database
@app.route('/collections/<database_name>', methods=['GET'])
def list_collections(database_name):
    collections = client[database_name].list_collection_names()
    return render_template('collections.html', collections=collections, database=database_name)



# Route to retrieve all documents from a collection
@app.route('/collections/<database_name>/<collection_name>', methods=['GET'])
def get_documents(database_name, collection_name):
    collection = client[database_name][collection_name]
    documents = list(collection.find())
    return render_template('documents.html', collection_name=collection_name, documents=documents)



if __name__ == '__main__':
    app.run(debug=True)