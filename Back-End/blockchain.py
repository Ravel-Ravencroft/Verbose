from datetime import date, datetime
from hashlib import sha256

class Block:
    def __init__(self, student_id, date, time, previous_hash):
        self.student_id = student_id
        self.date = date
        self.time = time
        self.previous_hash = previous_hash

    def compute_hash(self):
        return sha256( self.compute_hash_string().encode() ).hexdigest()

    def compute_hash_string(self):
        return '{} {} - {}'.format(self.date + " " + self.time, self.student_id, self.previous_hash)

    def parse_json(self):
        return {"id": self.student_id, "date": self.date, "time": self.time, "hash": self.previous_hash}

class Blockchain:
    DEFAULT_HASH = sha256( "The Default Hash".encode() ).hexdigest()
    chain = []

    def add_block(self, student_id, previous_hash, timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        self.chain.append( Block(student_id, timestamp.split(" ")[0], timestamp.split(" ")[1], previous_hash) )

    # Rename to generate_student_list
    def generate_student_list(self, student_id = None, date = None):
        data = []
        for block in self.chain:
            if student_id is not None and block.student_id != student_id:
                continue
            if date is not None and block.date != date:
                continue

            data.append( {'date': block.date, 'time': block.time} )

        return data

    def generate_day_list( self, date = date.today().strftime('%Y-%m-%d'), ids = None, json = True ):
        data = []
        
        for block in reversed(self.chain):
            if block.date != date:
                continue
            if ids is not None and block.student_id not in ids:
                continue

            data.append( {'id': block.student_id, 'time': block.timestamp[11:]} )
            ids.remove(block.student_id)

        for id in ids:
            data.append( {'id': id, 'time': None} )

        if json:
            return {'date': date, 'details': data}
        else:
            return data

    def print_blockchain(self):
        print("\nThe Blockchain")
        for block in self.chain:
            print( block.compute_hash_string() )
