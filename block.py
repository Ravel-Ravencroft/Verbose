from hashlib import sha256
from datetime import datetime

class Block:
    def __init__(self, student_id, previous_hash):
        self.student_id = student_id
        self.previous_hash = previous_hash
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.hash_string = '{} {} - {}'.format(self.timestamp, student_id, previous_hash)

    def compute_hash(self):
        return sha256(self.hash_string.encode()).hexdigest()

    def print_details(self):
        return ("\nStudent ID: " + self.student_id + "\nTimestamp: " + self.timestamp + "\n")
