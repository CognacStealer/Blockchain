# Merkle Trees from scratch — Python and JavaScript

Me working through how a Merkle tree actually gets built, in two languages, to
make sure I understood the structure rather than just the diagram of it.

A Merkle tree lets you prove that one transaction is part of a block without
handing someone the whole block. You hash every transaction, hash the hashes
pairwise, and keep going until one root hash is left. Change any single
transaction anywhere below and the root changes — which is the whole point.

```
                 root
                /    \
           H(AB)      H(CD)
           /   \      /   \
        H(A)  H(B)  H(C)  H(D)
          |     |     |     |
          A     B     C     D      ← transactions
```

The detail that took me a moment: when a level has an **odd** number of nodes,
the last hash is duplicated so it can be paired with itself. That's what
Bitcoin does, and it's why the tree is always a clean binary structure even
when the transaction count isn't a power of two.

## Files

| File | What it is |
|---|---|
| `merkletree.py` | Python version — build, proof generation, proof verification |
| `merkletree.js` | JavaScript version of the same thing |
| `test_merkletree.py` | 11 property tests over the Python version |
| `main.py` | Stub from `uv init`, not used |

## Proofs are the point

A tree with no proof method isn't doing anything a plain hash wouldn't. So both
versions generate and verify **Merkle proofs**: the sibling hashes along the path
from one transaction up to the root.

```
proof for Tx3 = [ hash(Tx4), hash(Tx1Tx2), hash(Tx5Tx5-subtree) ]
```

Three hashes, not five transactions. For n transactions a proof is log2(n)
hashes — that's what makes this structure worth building. You hand someone one
transaction plus three hashes, they recompute the root, and either it matches or
the transaction isn't in the block.

The demo at the bottom of each file verifies a real transaction (`True`), then
feeds a **tampered** version of it — `Charlie pays Dave 3 BTC` instead of `2` —
against the same proof, which must come back `False`.

## Running it

```bash
python merkletree.py
node merkletree.js
python test_merkletree.py
```

Both implementations produce the **same root** for the same transactions:

```
037f343e919ab09c512a799fe0b5d2fed89c4bc1c439020404d654e98ccb7cc0
```

No dependencies — `hashlib` in Python, Node's builtin `crypto` in JavaScript.

## What was wrong before

The Python file used to be broken, in two ways worth recording:

1. **`buildtree` stopped mid-statement** — `for i in range(0)` with no body. The
   file didn't even parse.
2. **`calculateHash` hashed its input twice.** It called `SHA256.new(data)` and
   *then* `hash_obj.update(data)`, so the digest was `SHA256(data + data)`, not
   `SHA256(data)`. That one is nastier than the syntax error: it produces
   perfectly valid-looking 64-character hashes that are silently wrong and match
   no other SHA-256 implementation on earth. The parity check against the JS
   version is what would have caught it.

It also imported `Crypto.Hash` from pycryptodome, which isn't a dependency of
this project. `hashlib` does the same job and mirrors what the JS side uses.
