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
