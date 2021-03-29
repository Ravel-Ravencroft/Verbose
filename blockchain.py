from block import Block

class Blockchain:
    blockchain = []
    genesis_block = Block('w1761000', 'Beginning to Work Well')
    
    block1 = Block('w1761053', genesis_block.compute_hash())

    # print(block1)
    print(block1.print_details())

    def start_functionality(self):
        if not Blockchain().blockchain:
            Blockchain().blockchain.append(Blockchain().genesis_block)

    def end_functionality(self):
        self.print_blockchain()

    def print_blockchain(self):
        print("The Blockchain")
        for block in self.blockchain:
            print(block.hash_string)

Blockchain().start_functionality()

Blockchain().print_blockchain()

block = Block( 'w1761053', Blockchain().blockchain[-1].compute_hash() )
Blockchain().blockchain.append(block)

print(block.print_details())

Blockchain().end_functionality()
