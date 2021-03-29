from datetime import datetime
from hashlib import sha256

class Block:
    def __init__(self, student_id, previous_hash, timestamp):
        self.student_id = student_id
        self.previous_hash = previous_hash
        self.timestamp = timestamp

    def compute_hash(self):
        return sha256( self.compute_hash_string().encode() ).hexdigest()

    def compute_hash_string(self):
        return '{} {} - {}'.format( self.timestamp, self.student_id, self.previous_hash)

    def to_string(self):
        return ( {'id': self.student_id, 'timestamp': self.timestamp} )

class Blockchain:
    DEFAULT_HASH = sha256( "The Default Hash".encode() ).hexdigest()
    chain = []

    def add_block(self, student_id, previous_hash = DEFAULT_HASH if not chain else chain[-1].compute_hash(), timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        self.chain.append( Block(student_id, previous_hash, timestamp) )

    def generate_json(self, student_id = None, start_date = None, end_date = None):
        data = []
        for block in self.chain:
            if student_id is not None and block.student_id != student_id:
                continue

            elif start_date is not None and block.timestamp[0:10] < start_date:
                continue

            elif end_date is not None and block.timestamp[0:10] > end_date:
                break

            data.append( block.to_string() )

        return data

    def print_blockchain(self):
        print("\nThe Blockchain")
        for block in self.chain:
            print( block.compute_hash_string() )
