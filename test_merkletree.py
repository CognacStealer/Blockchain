"""
Tests for merkletree.py. Run: python test_merkletree.py

These are the properties that matter for a Merkle tree. If any of them fails,
the tree isn't proving anything.
"""

import hashlib
from merkletree import MerkleTree, calculate_hash

TXS = [
    "Tx1: Alice pays Bob 10 BTC",
    "Tx2: Bob pays Charlie 5 BTC",
    "Tx3: Charlie pays Dave 2 BTC",
    "Tx4: Dave pays Eve 1 BTC",
    "Tx5: Eve pays Frank 0.5 BTC",
]


def test_hash_is_plain_sha256():
    # The original double-fed the data (SHA256.new(data) then .update(data)),
    # producing SHA256(data + data). This pins the correct behaviour.
    assert calculate_hash("abc") == hashlib.sha256(b"abc").hexdigest()
    assert calculate_hash("abc") == calculate_hash(b"abc")


def test_root_is_deterministic():
    assert MerkleTree(TXS).root == MerkleTree(TXS).root


def test_any_change_changes_the_root():
    original = MerkleTree(TXS).root
    for i in range(len(TXS)):
        tampered = list(TXS)
        tampered[i] = tampered[i] + " "
        assert MerkleTree(tampered).root != original, f"tampering tx {i} left the root unchanged"


def test_order_matters():
    assert MerkleTree(TXS).root != MerkleTree(list(reversed(TXS))).root


def test_proof_verifies_for_every_transaction():
    tree = MerkleTree(TXS)
    for tx in TXS:
        proof = tree.get_merkle_proof(tx)
        assert MerkleTree.verify_merkle_proof(tx, proof, tree.root), f"proof failed for {tx}"


def test_proof_rejects_a_tampered_transaction():
    tree = MerkleTree(TXS)
    target = "Tx3: Charlie pays Dave 2 BTC"
    proof = tree.get_merkle_proof(target)
    fake = "Tx3: Charlie pays Dave 3 BTC"
    assert not MerkleTree.verify_merkle_proof(fake, proof, tree.root)


def test_proof_is_logarithmic():
    # 5 txs pad to 6 -> 4 -> 2 -> 1, so 3 sibling hashes, not 5.
    assert len(MerkleTree(TXS).get_merkle_proof(TXS[0])) == 3


def test_odd_and_even_counts_both_build():
    for n in range(1, 10):
        tree = MerkleTree([f"tx{i}" for i in range(n)])
        assert isinstance(tree.root, str) and len(tree.root) == 64
        for tx in tree.transactions:
            proof = tree.get_merkle_proof(tx)
            assert MerkleTree.verify_merkle_proof(tx, proof, tree.root), f"n={n} failed for {tx}"


def test_single_transaction():
    tree = MerkleTree(["only one"])
    assert tree.root == calculate_hash("only one")
    assert tree.get_merkle_proof("only one") == []


def test_empty_is_rejected():
    try:
        MerkleTree([])
    except ValueError:
        return
    raise AssertionError("empty transaction list should raise")


def test_unknown_transaction_is_rejected():
    try:
        MerkleTree(TXS).get_merkle_proof("never happened")
    except ValueError:
        return
    raise AssertionError("unknown transaction should raise")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  pass  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
