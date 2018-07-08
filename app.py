from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin
import psycopg2
import os

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
conn = psycopg2.connect("host='ec2-54-197-253-122.compute-1.amazonaws.com' dbname='df3192mkr3k3ch' user='egtavjsibewktj' password='51fa705edf6ebe7f7e7e3f2223b9768386741a7d91bc731931820e2c7dc8f95d'")
cur = conn.cursor()
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("select name from phone")
conn.commit()
phones = cur.fetchall()
data = []
for phone in phones:
    data.append(phone[0])

@cross_origin()
@app.route('/', methods=['GET'])
def home(name=None):
    return '''<h1>Distant Reading Archive</h1>
            <p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/phones', methods=['GET'])
def get_phones():
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)