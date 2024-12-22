import hashlib
import time
import json
from typing import List

class MerkleTree:
    def __init__(self, transactions: List[str]):
        self.transactions = transactions
        self.root = self.build_merkle_root(transactions)

    def build_merkle_root(self, transactions: List[str]) -> str:
        if len(transactions) == 1:
            return self.hash(transactions[0])

        new_level = []
        for i in range(0, len(transactions), 2):
            left = transactions[i]
            right = transactions[i + 1] if i + 1 < len(transactions) else left
            combined_hash = self.hash(left + right)
            new_level.append(combined_hash)

        return self.build_merkle_root(new_level)

    @staticmethod
    def hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()


class Block:
    def __init__(self, previous_hash: str, transactions: List[str]):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.merkle_root = MerkleTree(transactions).root
        self.hash = None
        self.nonce = 0

    def mine_block(self, difficulty: int):
        prefix = '0' * difficulty
        while not self.hash or not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_data = {
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce
        }
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()


class Blockchain:
    def __init__(self, difficulty: int):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("0", ["Genesis Block"])
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, transactions: List[str]):
        previous_hash = self.chain[-1].hash
        new_block = Block(previous_hash, transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def validate_blockchain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.compute_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Demonstration of the Blockchain
if __name__ == "__main__":
    blockchain = Blockchain(difficulty=4)

    # Add transactions to the blockchain
    transactions1 = [
        "Alice sends 10 BTC to Bob",
        "Bob sends 5 BTC to Charlie",
        "Charlie sends 2 BTC to David",
        "David sends 1 BTC to Alice",
        "Alice sends 3 BTC to Bob",
        "Bob sends 2 BTC to Charlie",
        "Charlie sends 1 BTC to David",
        "David sends 1 BTC to Alice",
        "Alice sends 2 BTC to Bob",
        "Bob sends 1 BTC to Charlie"
    ]

    blockchain.add_block(transactions1)

    # Validate blockchain
    is_valid = blockchain.validate_blockchain()
    print(f"Blockchain valid: {is_valid}")

    # Print blockchain details
    for i, block in enumerate(blockchain.chain):
        print(f"Block {i}:")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Merkle Root: {block.merkle_root}")
        print(f"  Hash: {block.hash}\n")
