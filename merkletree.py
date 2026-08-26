from Crypto.Hash import SHA256

def calculateHash(data):
    hash_obj = SHA256.new(data)
    print(hash_obj.digest())
    hash_obj.update(data)
    return hash_obj.hexdigest()
    

class MerkleTree():
    def __init__(self , transactions):
        self.transactions = transactions
        self.levels = []
        self.root = self.buildtree()


    def buildtree(self):
        level = [calculateHash(tx) for tx in self.transactions]
        self.levels.append(level)


        while len(level) > 1:
            if len(level) % 2 != 0:
                level.append(level[-1])

            next_level = []

            for i in range(0)




r = "Hello"

print(calculateHash(r.encode('utf-8')))