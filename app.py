#simple web app that serves data.json
from collections import deque

from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)

@app.route('/data')
def data():
    limit = request.args.get('limit')
    with open("data.json", "r") as f:
        entries = json.load(f)
        entries: list[dict[str,int]]
    if limit:
        entries = list(deque(entries, maxlen=int(limit)))
    return jsonify(entries)

#start the server
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
