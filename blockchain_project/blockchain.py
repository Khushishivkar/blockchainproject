import hashlib
import json
from time import time
from flask import Flask, jsonify, request

# -------------------------------
# Blockchain Class
# -------------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_donations = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """Create a new block in the blockchain"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'donations': self.current_donations,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset current donations
        self.current_donations = []
        self.chain.append(block)
        return block

    def new_donation(self, donor_id, donor_name, amount, organization):
        """Add a new donation to the list of current donations"""
        self.current_donations.append({
            'donor_id': donor_id,
            'donor_name': donor_name,
            'amount': float(amount),  # convert amount to float
            'organization': organization
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """Create a SHA-256 hash of a block"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def home():
    return '''
    <h2>💸 Blockchain-Based Donation Tracking System</h2>
    <p>This decentralized app records donations securely on a blockchain ledger.</p>

    <form action="/donate" method="post">
        <input type="text" name="donor_id" placeholder="Donor ID" required><br><br>
        <input type="text" name="donor_name" placeholder="Donor Name" required><br><br>
        <input type="number" name="amount" placeholder="Donation Amount" required><br><br>
        <input type="text" name="organization" placeholder="Organization Name" required><br><br>
        <button type="submit">Donate</button>
    </form>

    <p>View full blockchain: <a href="/chain">/chain</a></p>
    '''

@app.route('/donate', methods=['POST'])
def donate():
    donor_id = request.form.get('donor_id')
    donor_name = request.form.get('donor_name')
    amount = request.form.get('amount')
    organization = request.form.get('organization')

    # Add donation to the blockchain
    index = blockchain.new_donation(donor_id, donor_name, amount, organization)
    block = blockchain.new_block(proof=12345)

    return jsonify({
        'message': '✅ Donation successfully recorded!',
        'block': block
    }), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5000)
