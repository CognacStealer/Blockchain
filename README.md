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
| `merkletree.py` | Python version, SHA-256 via `pycryptodome` |
| `merkletree.js` | JavaScript version of the same thing |
| `main.py` | Stub from `uv init`, not used |

## Status — this is unfinished

**`merkletree.py` does not run.** The `buildtree` method stops mid-way through
the pairing loop:

```python
for i in range(0)     # ← incomplete, no body
```

I left it where I stopped. What's still to do:

- [ ] finish the pairing loop — step `i` by 2, concatenate `level[i] + level[i+1]`, hash, append to `next_level`
- [ ] assign `level = next_level` and append it to `self.levels` each round
- [ ] return the final single hash as the root
- [ ] remove the stray `print(hash_obj.digest())` inside `calculateHash` — it's debug output
- [ ] fix the double-hashing bug in `calculateHash`: it calls `SHA256.new(data)` *and then* `hash_obj.update(data)`, so the data gets fed in twice and the digest is `SHA256(data + data)`, not `SHA256(data)`
- [ ] add a `get_proof(tx)` method returning the sibling hashes along the path — a tree with no proof method isn't doing anything a plain hash wouldn't

## Running it

```bash
uv sync           # or: pip install pycryptodome
python merkletree.py
node merkletree.js
```
