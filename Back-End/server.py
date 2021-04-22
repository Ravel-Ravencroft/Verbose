import atexit
import json

from datetime import date
from hashlib import sha256
from os import path, remove

from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_restful import Api, Resource

from blockchain import Blockchain
from config import INSTITUTE_ID, INSTITUTE_NAME, INSTITUTE_START_TIME as time
from emailer import send_email

#START OF BACK-END PROCESSES SEGMENT

FILE_NAME = "serverBlockchain.json"
FILE_NAME_REGISTER = "classRegister.json"

GENESIS_HASH = sha256( INSTITUTE_NAME.encode() ).hexdigest()
GENESIS_TIMESTAMP = "2021-04-01 00:00:00"

blockchain = Blockchain()

def start_blockchain_functionality():
    blockchain.add_block(INSTITUTE_ID, GENESIS_HASH, GENESIS_TIMESTAMP)

    if path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            data = json.loads( file.read() )

        for item in data:
            if blockchain.chain[-1].compute_hash() == item["hash"]:
                blockchain.add_block(item["id"], item["hash"], item["date"] + " " + item["time"])

            else:
                print( "Hash Correspondence Suspicion on Entry: " + str( len(blockchain.chain) ) )
                print( blockchain.chain[-1].parse_json() )
                break
        
        if (len(blockchain.chain) - 1) != len(data):
            return False
        else:
            print("\n" + str(len(blockchain.chain) - 1) + " Records Have Been Parsed into the Chain!\n")
            return True


def get_attendance(id, date):
    if path.exists(FILE_NAME_REGISTER):
        with open(FILE_NAME_REGISTER, "r") as file:
            array = json.loads( file.read() )

        for item in array:
            if item["id"] == id:
                # print( blockchain.generate_day_list(ids = item['ids'], date = date) )
                return blockchain.generate_day_list(ids = item['ids'], date = date)


def get_ids(student):
    if path.exists(FILE_NAME_REGISTER):
        with open(FILE_NAME_REGISTER, "r") as file:
            array = json.loads( file.read() )

        ids = []
        for item in array:
            if student is True:
                for id in item['ids']:
                    ids.append(id)
            else:
                ids.append(item['id'])

        return ids
    else:
        print("The classRegister.json file is missing or inaccessible. Please Contact the IT Department!")


def send_lists():
    if path.exists(FILE_NAME_REGISTER):
        with open(FILE_NAME_REGISTER, "r") as file:
            array = json.loads( file.read() )

        for item in array:
            blockchain_data = blockchain.generate_day_list( ids = item['ids'], date = date.today().strftime('%Y-%m-%d') )

            send_email({"id": item["id"], "email": item["email"], "data": blockchain_data})

        print("\nAttendance Lists Sent!\n")

    else:
        print("The classRegister.json file is missing or inaccessible. Please Contact the IT Department!")


def end_functionality():
    if len(blockchain.chain) != 0:
        with open(FILE_NAME, "w") as file:
            data = []
            for block in blockchain.chain:
                if block is blockchain.chain[0]:
                    continue
                
                data.append( block.parse_json() )

            file.write( json.dumps(data, indent = 4) )

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

class Class(Resource):
    def get(self, id, date):
        return get_attendance(str.lower(id), date)

class Student(Resource):
    def get(self, id):
        return blockchain.generate_student_list( str.lower(id) )

class Students(Resource):
    def get(self):
        return { blockchain.generate_student_list() }


api.add_resource(Documentation, '/')

api.add_resource(Class, '/class/<string:id>/<string:date>')

api.add_resource(Student, '/student/<string:id>')

api.add_resource(Students, '/students')


if __name__ == '__main__':
    if start_blockchain_functionality():
        scheduler.init_app(app)
        scheduler.add_job(id = "Scheduled Email", func = send_lists, trigger = 'cron', hour = time[0:2], minute = time[3:])
        scheduler.start()
        app.run(debug = False)

#END OF FLASK SEGMENT