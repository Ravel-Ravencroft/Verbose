from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)
api = Api(app)

blockchain_object = Blockchain()
blockchain_object.start_functionality()

class Documentation(Resource):
    def get(self):
        return { "data": "Documentation Page Goes Here!" }

class Student(Resource):
    def get(self, id = None, start_date = None, end_date = None):
        return { "id": id , "data": blockchain_object.generate_json(id, start_date, end_date) }

class Students(Resource):
    def get(self):
        return { "data": blockchain_object.generate_json() }


api.add_resource(Documentation, '/')

api.add_resource(Student, '/student/<string:id>',
                            '/student/<string:id>/<string:start_date>',
                            '/student/<string:id>/<string:start_date>/<string:end_date>')

api.add_resource(Students, '/students')


if __name__ == '__main__':
    app.run(debug = True)