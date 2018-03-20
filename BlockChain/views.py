from django.shortcuts import render,HttpResponse
from time import time
from uuid import uuid4

import json
import hashlib


class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set()

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # Storage transactions
        # Creates a new Block and adds it to the chain
        """
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
            return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof*proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"

node_identifier = str(uuid4()).replace("-", "")
# Instantiate the Blockchain
blockchain = Blockchain()


def mine(request):
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)
    print(proof)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)
    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    print(response)
    return HttpResponse(json.dumps(response))


def new_transaction(request):
    values = {
        "sender": "one address",
        "recipient": "the other address",
        "amount": 5
    }
    # values = json.dumps(values)
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values"
    index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])
    print(index)
    response = {"message": "Transaction will be added to Block %s"% index}
    return HttpResponse(json.dumps(response))


def full_chain(request):
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return HttpResponse(json.dumps(response))


def hash_text(request):

    return render(request, "hash.html")
