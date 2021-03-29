from flask import Flask, jsonify
from blockchain import Blockchain

app = Flask(__name__)

blockchain_object = Blockchain()
blockchain_object.start_functionality()

@app.route('/blockchain/<str:id>', method=['GET'])
def get_student_records(id):
    return jsonify( {"id": id, "data": blockchain_object.generate_json()} )

@app.route('/blockchain')
def hello_blockchain():
    return jsonify( {"data": blockchain_object.generate_json()} )

if __name__ == '__main__':
    app.run(debug = True)