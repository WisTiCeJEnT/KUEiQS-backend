from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return "Working"

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    print(data)
    return jsonify({"status": "ok", "table": [["01204111", "Compro", "Jui's Room", "24/7"],["01999111", "kotl", "E201", "09001200"]]})

if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0", port=5000)
