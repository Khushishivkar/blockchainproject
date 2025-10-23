from flask import Flask, jsonify
from blockchain import blockchain  # Import your blockchain instance

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/')
def home():
    return "<h2>🚀 Welcome to Your Local Blockchain Explorer</h2><p>Visit <a href='/chain'>/chain</a> to view the full blockchain.</p>"

if __name__ == '__main__':
    app.run(port=5000)
