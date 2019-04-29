from flask import Flask, request, jsonify
from flask_cors import CORS
import ku_eiqs

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return "Working"

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    #print(data)
    data = ku_eiqs.nontri_login(data)
    return jsonify(data)

@app.route('/examtbl', methods=['GET', 'POST'])
def examTbl():
    data = request.get_json()
    print(data)
    return jsonify({"status": "ok"})

@app.route('/getdata', methods=['GET', 'POST'])
def getData():
    data = request.get_json()
    print(data)
    data = ku_eiqs.query_data(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0", port=5000)
