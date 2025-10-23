import hashlib
import json
from time import time
import streamlit as st

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
            'amount': float(amount),
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
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Blockchain Donation Tracker", page_icon="💸")
st.title("💸 Blockchain-Based Donation Tracking System")

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# -------------------------------
# Donation Form
# -------------------------------
st.subheader("Add a Donation")
with st.form("donation_form"):
    donor_id = st.text_input("Donor ID")
    donor_name = st.text_input("Donor Name")
    amount = st.number_input("Donation Amount", min_value=0.0, step=1.0)
    organization = st.text_input("Organization Name")
    submitted = st.form_submit_button("Donate")

    if submitted:
        if donor_id and donor_name and amount > 0 and organization:
            blockchain.new_donation(donor_id, donor_name, amount, organization)
            block = blockchain.new_block(proof=12345)
            st.success(f"✅ Donation recorded in block #{block['index']}!")
        else:
            st.error("Please fill in all fields and provide a valid amount.")

# -------------------------------
# Show Full Blockchain
# -------------------------------
st.subheader("Full Blockchain")
if st.button("Show Blockchain"):
    st.json(blockchain.chain)
