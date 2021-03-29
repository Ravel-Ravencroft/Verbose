from datetime import datetime
from hashlib import sha256
from os import path

class Block:
    def __init__( self, student_id, previous_hash, timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') ):
        self.student_id = student_id
        self.previous_hash = previous_hash
        self.timestamp = timestamp

    def compute_hash(self):
        return sha256(self.compute_hash_string().encode()).hexdigest()

    def compute_hash_string(self):
        return '{} {} - {}'.format(self.timestamp, self.student_id, self.previous_hash)

    def to_string(self):
        return ( {"Student ID": self.student_id, "Timestamp": self.timestamp} )

class Blockchain:
    genesis_block = Block('u5700600', 'Informatics Institute of Technology')
    chain = []

    def add_block(self, student_id):
        if not self.chain:
            self.chain.append(self.genesis_block)

        self.chain.append( Block( student_id, self.chain[-1].compute_hash() ) )

    def end_functionality(self):
        file = open("demofile.txt", "w")
        for block in self.chain:
            file.write( block.compute_hash_string() + "\n" )
        file.close()

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

    def start_functionality(self):
        if( path.exists("demofile.txt") ):
            file = open("demofile.txt", "r")
            for line in file:
                self.chain.append( Block(line[20:28], line[31:].rstrip("\n"), line[0:19]) )
        else:
            self.chain.append(self.genesis_block)
        
        print( len(self.chain) )

# blockchain_object = Blockchain()

# blockchain_object.start_functionality()

# test_block = blockchain_object.add_block('w1761053')
# print( blockchain_object.chain[-1].to_string() )

# print( blockchain_object.generate_json() )

# print( blockchain_object.generate_json("w1761077", "2021-03-01", "2021-03-07") )

# blockchain_object.end_functionality()