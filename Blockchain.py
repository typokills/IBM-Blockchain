from hashlib import sha256
import json
import time

class Block:
    def __init__(self,index,transactions,timestamp, previous_hash):
        self.index = index #Block ID
        self.transactions = transactions
        self.timestamp = timestamp # Time of generation of the block
        self.previous_hash = previous_hash

    #Addition of Hash Function 
    #Requirements: Easy to compute, deterministic, uniformly random
    #Consequence: Impossible to guess input, input + hash = output
    def compute_hash(block):
        #Returns the hash of the block
        block_string = json.dumps(self.__dict__,sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    

class Blockchain:
    # difficulty of PoW algorithm
    difficulty = 2

    def __init__(self):
        self.chain = [] #Uses a list to store the blocks
        self.create_genesis_block() #creates the first block and adds it to the chain
        self.unconfirmed_transactions = []
    def create_genesis_block():
        genesis_block = Block(0,[],time.time(),'0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self,block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_block(self,block,proof):
        # Adds block after verification 
        # Checks if the proof is valid
        #previous_hash referred in the block and the hash of a
        previous_hash = self.last_block.hash

        #Check 1: Previous hash links to the current block's previous hash
        if previous_hash != block.previous_hash:
            return False

        #Check 2: Checks if the hash of the block matches the difficulty level
        if not Blockchain.is_valid_proof(block,proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self,block,block_hash):
        return(block_hash.startswith(0*Blockchain.difficulty) and 
            block_hash == block.compute_hash())

    def add_new_transaction(self,transaction):
        self.unconfirmed_transactions.append(transaction)
    
    # mine function add pending transactions to the block and figuring out the proof of work
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
    
        last_block = self.last_block
        
        new_block = Block(index=last_block.index + 1, 
                          transactions = self.unconfirmed_transactions,
                          timestamp = time.time(),
                          previous_hash = last_block.hash)

        proof = self.proof_of_work(new_block) #
        self.add_block(new_block,proof) #Adds new block to the blockchain
        self.unconfirmed_transactions = [] #Resets the unconfirmed_transactions
        return new_block.index

from flask import Flask, request
import requests 

app = Flask(__name__)

blockchain = Blockchain()
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ['author', 'content']

    for field in required_fields:
        if not tx_data.get(field):
            return 'Invalid transaction data', 404
    
    tx_data['timestamp'] = time.time()

    blockchain.add_new_transaction(tx_data)

    return 'Success', 201

data = b'0'
data2 = b'1'
print(sha256(data).hexdigest())
print(sha256(data2).hexdigest())