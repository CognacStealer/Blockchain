const crypto = require("crypto");

// sha256 function
function calculateHash(data){
    return crypto
    .createHash("sha256")
    .update(data)
    .digest("hex");

}

class MerkleTree{
    constructor(transactions){
        this.transactions = transactions;
        this.levels = [];
        this.root = this.buildTree();
    }

    buildTree(){
        // leaf node creation

        let level = this.transactions.map(tx => calculateHash(tx));
        this.levels.push(level);

        // Build tree
        while(level.length > 1){
    
            // Duplicate last hash if there are odd number of transactions
            if (level.length % 2 !== 0)
                level.push(level[level.length - 1]);
        

            let nextlevel = [];

            for (let i = 0; i < level.length; i += 2) {
                nextlevel.push(calculateHash(level[i] + level[i + 1]));
            }
            
            this.levels.push(nextlevel);  //push complete level to levels
            level = nextlevel;
        }
        // Final root
        return level[0];
    }

    // Display Tree
    printTree() {

        console.log("\nMerkle Tree");

        for (let i = 0; i < this.levels.length; i++) {    //traverse through each level

            console.log("\nLevel " + i);

            for (let j = 0; j < this.levels[i].length; j++) {       // traverse through each hash in that level

                console.log(this.levels[i][j]);

            }

        }

    }

    // Generate Merkle Proof for a transaction
  getMerkleProof(transaction) {
    let index = this.transactions.indexOf(transaction);

    if (index === -1) {
      throw new Error("Transaction not found in the tree");
    }

    let proof = [];

    // Traverse each level except the root
    for (let level = 0; level < this.levels.length - 1; level++) {
      let currentLevel = this.levels[level];

      let isRightNode = index % 2 == 1;
      let siblingIndex = isRightNode ? index - 1 : index + 1;

      proof.push({
          hash: currentLevel[siblingIndex],
          position: isRightNode ? "left" : "right"
        });

      // Move to parent index
      index = Math.floor(index / 2);
    }

    return proof;
  }

  // Verify Merkle Proof
  static verifyMerkleProof(transaction, proof, root) {
    let currentHash = calculateHash(transaction);

    for (const step of proof) {
      if (step.position == "left") {
        currentHash = calculateHash(step.hash + currentHash);
      } else {
        currentHash = calculateHash(currentHash + step.hash);
      }
    }
    
    return currentHash == root;
  }

}

const transactions = [
  "Tx1: Alice pays Bob 10 BTC",
  "Tx2: Bob pays Charlie 5 BTC",
  "Tx3: Charlie pays Dave 2 BTC",
  "Tx4: Dave pays Eve 1 BTC",
  "Tx5: Eve pays Frank 0.5 BTC"
];

const merkleTree = new MerkleTree(transactions);
merkleTree.printTree();

console.log("\nMerkle Root:");
console.log(merkleTree.root);

const targetTx = "Tx3: Charlie pays Dave 2 BTC";

// Generate Merkle Proof
const proof = merkleTree.getMerkleProof(targetTx);

console.log("\nMerkle Proof for transaction:");
console.log(proof);

//Verify Merkle Proof
const isValid = MerkleTree.verifyMerkleProof(
  targetTx,
  proof,
  merkleTree.root
);

console.log("\nIs Merkle Proof valid?", isValid);


//Simulation of when a fake transaction is given with a valid merkle proof for verificaion
const fakeTrans = "Tx3: Charlie pays Dave 3 BTC";

// Verify Merkle Proof
const isValid1 = MerkleTree.verifyMerkleProof(
  fakeTrans,
  proof,
  merkleTree.root
);

console.log("\nIs Merkle Proof valid?", isValid1);