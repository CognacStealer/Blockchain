import hashlib 
import time 
import json


class Block:
    def __init__(self , timestamp , data , previous_hash):
        self.timestamp = timestamp
        self.data = data 
        self.previous_hash = previous_hash
        self.hash = ""

    def calculate_hash(self):
        value = str(self.timestamp) + json.dumps(self.data) + self.previous_hash
        return hashlib.sha256(value.encode()).hexdigest()

    def to_dict(self):
        return {
            "timestamp" : self.timestamp , 
            "data" : self.data,
            "previous_hash" : self.previous_hash,
            "hash" : self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_gensis()]

    def create_gensis(self):
        gen_block = Block(int(time.time() * 1000) , "Gensis" , "0")
        gen_block.hash = gen_block.calculate_hash()
        return gen_block

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self , data):
        previous_hash = self.get_latest_block().hash
        new_block = Block(int(time.time() * 1000) , data , previous_hash)
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
            for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i - 1]
    
                if current_block.hash != current_block.calculate_hash():
                    print("Block is Tempered")
                    return False
    
                if current_block.previous_hash != previous_block.hash:
                    print("Chain is Broken")
                    return False
    
            return True
    
    def to_dict(self):
            return {"chain": [block.to_dict() for block in self.chain]}
    

chain2 = Blockchain()

chain2.add_block({"Sender":"A" , "Receiver":"B", "amount" : "250"})
chain2.add_block({"Sender":"B" , "Receiver":"A", "amount" : "150"})


print(json.dumps(chain2.to_dict() , indent= 4))

print("Check my chain", chain2.is_chain_valid())


chain2.chain[1].data = ({"Sender":"A" , "Receiver" : "B" , "amount":"100"})

print("Check my chain", chain2.is_chain_valid())

chain2.chain[1].hash = chain2.chain[1].calculate_hash()


print("Check my chain", chain2.is_chain_valid())
