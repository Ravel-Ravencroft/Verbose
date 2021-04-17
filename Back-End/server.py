import atexit
from hashlib import sha256
from os import path
from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_restful import Api, Resource
from blockchain import Blockchain
import emailer as Emailer
from pdf_generator import PDFGenerator as Generator

#START OF BACK-END PROCESSES SEGMENT

FILE_NAME = "serverBlockchain.txt"
GENESIS_ID = "u5700600"
GENESIS_HASH = sha256( "Informatics Institute of Technology".encode() ).hexdigest()
GENESIS_DATE = "2021-01-01 00:00:00"

ON_TIME = "07:25" #TODO: Edit for Institute's Time as Required.

blockchain = Blockchain()
generator = Generator()

def start_blockchain_functionality():
    blockchain.add_block(GENESIS_ID, GENESIS_HASH, GENESIS_DATE)

    if( path.exists(FILE_NAME) ):
        file = open(FILE_NAME, "r")

        for line in file:
            id = line[20:28]
            previous_hash = line[31:].rstrip("\n")
            timestamp = line[0:19]

            if(blockchain.chain[-1].compute_hash() == previous_hash):
                blockchain.add_block(id, previous_hash, timestamp)
            else:
                # TODO: Add Functionality to Handle Blockchain Tampering.
                pass

    print("\n" + str(len(blockchain.chain) - 1) + " Records Have Been Parsed into the Chain!\n")


def end_functionality():
    file = open(FILE_NAME, "w")
    for block in blockchain.chain:
        if(block is blockchain.chain[0]):
            continue

        file.write(block.compute_hash_string() + "\n")

    file.close()

    print("\nThe Blockchain File has Been Written To!\n")

atexit.register(end_functionality)

#END OF BACK-END PROCESSES SEGMENT

#START OF FLASK SEGMENT

app = Flask(__name__)
CORS(app)
api = Api(app)
scheduler = APScheduler()
scheduler.api_enabled = True

class Documentation(Resource):
    def get(self):
        return { "data": "Documentation Page Goes Here!" }

class Student(Resource):
    def get(self, id = None):
        return { "id": id , "data": blockchain.generate_json(id) }

class Students(Resource):
    def get(self):
        return { "data": blockchain.generate_json() }


api.add_resource(Documentation, '/')

api.add_resource(Student, '/student/<string:id>')

api.add_resource(Students, '/students')

def send_list():
    generator.create_pdf()
    Emailer.send_email()
    print("\nEmail Sent!\n")

if __name__ == '__main__':
    start_blockchain_functionality()
    scheduler.init_app(app)
    scheduler.add_job(id = "Scheduled Email", func = send_list, trigger = 'cron', hour = ON_TIME[0:2], minute = ON_TIME[3])
    scheduler.start()
    app.run(debug = False)

#END OF FLASK SEGMENT
