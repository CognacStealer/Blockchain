"""
Merkle tree — Python implementation.

Mirrors merkletree.js so the two can be compared side by side; both produce the
same root for the same transactions.

Uses hashlib from the standard library. The original used Crypto.Hash from
pycryptodome, which isn't a dependency of this project and isn't needed — the
JS version uses Node's builtin crypto, so hashlib is the honest counterpart.
"""

import hashlib


def calculate_hash(data):
    """SHA-256 of data, as a hex string. Accepts str or bytes."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


class MerkleTree:
    def __init__(self, transactions):
        if not transactions:
            raise ValueError("a Merkle tree needs at least one transaction")
        self.transactions = list(transactions)
        self.levels = []
        self.root = self.build_tree()

    def build_tree(self):
        # Leaf level: hash every transaction.
        level = [calculate_hash(tx) for tx in self.transactions]

        while True:
            # An odd level can't be paired, so the last hash is duplicated and
            # paired with itself. This is what Bitcoin does, and it's why the
            # tree stays a clean binary structure for any transaction count.
            if len(level) > 1 and len(level) % 2 != 0:
                level.append(level[-1])

            self.levels.append(level)

            if len(level) == 1:
                return level[0]

            # Hash each adjacent pair to form the level above.
            level = [
                calculate_hash(level[i] + level[i + 1])
                for i in range(0, len(level), 2)
            ]

    def print_tree(self):
        print("\nMerkle Tree")
        for i, level in enumerate(self.levels):
            print(f"\nLevel {i}")
            for h in level:
                print(h)

    def get_merkle_proof(self, transaction):
        """
        The sibling hashes needed to rebuild the root from one transaction.

        This is the whole point of a Merkle tree: it proves membership without
        handing over the other transactions. For n transactions the proof is
        log2(n) hashes, not n.
        """
        try:
            index = self.transactions.index(transaction)
        except ValueError:
            raise ValueError("Transaction not found in the tree")

        proof = []
        # Every level except the root contributes one sibling.
        for level in self.levels[:-1]:
            is_right_node = index % 2 == 1
            sibling_index = index - 1 if is_right_node else index + 1
            proof.append(
                {
                    "hash": level[sibling_index],
                    "position": "left" if is_right_node else "right",
                }
            )
            index //= 2

        return proof

    @staticmethod
    def verify_merkle_proof(transaction, proof, root):
        """Walk the proof up from the transaction and see if we land on root."""
        current = calculate_hash(transaction)
        for step in proof:
            if step["position"] == "left":
                current = calculate_hash(step["hash"] + current)
            else:
                current = calculate_hash(current + step["hash"])
        return current == root


if __name__ == "__main__":
    transactions = [
        "Tx1: Alice pays Bob 10 BTC",
        "Tx2: Bob pays Charlie 5 BTC",
        "Tx3: Charlie pays Dave 2 BTC",
        "Tx4: Dave pays Eve 1 BTC",
        "Tx5: Eve pays Frank 0.5 BTC",
    ]

    tree = MerkleTree(transactions)
    tree.print_tree()

    print("\nMerkle Root:")
    print(tree.root)

    target = "Tx3: Charlie pays Dave 2 BTC"
    proof = tree.get_merkle_proof(target)

    print("\nMerkle Proof for transaction:")
    for step in proof:
        print(f"  {step['position']:>5}  {step['hash']}")

    print("\nIs Merkle Proof valid?", MerkleTree.verify_merkle_proof(target, proof, tree.root))

    # Same proof, tampered transaction (3 BTC instead of 2). Must fail —
    # if this ever prints True, the tree is worthless.
    fake = "Tx3: Charlie pays Dave 3 BTC"
    print("Is Merkle Proof valid?", MerkleTree.verify_merkle_proof(fake, proof, tree.root))
