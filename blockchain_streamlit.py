import streamlit as st
from blockchain import Blockchain  # Import your blockchain class

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
