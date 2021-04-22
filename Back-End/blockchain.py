from datetime import date, datetime
from hashlib import sha256

class Block:
    def __init__(self, id, date, time, hash):
        self.student_id = id
        self.date = date
        self.time = time
        self.previous_hash = hash

    def compute_hash(self):
        return sha256( self.compute_hash_string().encode() ).hexdigest()

    def compute_hash_string(self):
        return '{} {} {} - {}'.format(self.date, self.time, self.student_id, self.previous_hash)

    def parse_json(self):
        return {"id": self.student_id, "date": self.date, "time": self.time, "hash": self.previous_hash}

class Blockchain:
    chain = []

    def add_block(self, id, hash, timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        self.chain.append( Block(id, timestamp.split(" ")[0], timestamp.split(" ")[1], hash) )

    def generate_student_list(self, student_id = None, date = None):
        data = []
        for block in self.chain:
            if student_id is not None and block.student_id != student_id:
                continue
            if date is not None and block.date != date:
                continue

            data.append( {'date': block.date, 'time': block.time} )

        return data

    def generate_day_list(self, ids, date):
        data = []
        
        for block in reversed(self.chain):
            if block.date < date:
                break
            if block.date > date:
                continue
            if block.student_id not in ids:
                continue

            data.append( {'id': block.student_id, 'time': block.time} )
            ids.remove(block.student_id)

        for id in ids:
            data.append( {'id': id, 'time': "-"} )

        return data

    def print_blockchain(self):
        print("\nThe Blockchain")
        
        for block in self.chain:
            print( block.compute_hash_string() )
