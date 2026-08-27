import hashlib 

def calculate_hash(data:str):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class MerkleTree:
    def __init__(self , trans):
        self.trans = trans
        self.levels = []
        self.root = self.build_tree()

    def build_tree(self):
        level = [calculate_hash(tx) for tx in self.trans]

        while True:
            if len(level) > 1 and len(level) % 2 != 0:
                level.append(level[-1])

            self.levels.append(level)

            if len(level) == 1:
                return level[0]

            level = [calculate_hash(level[i] + level[i+1]) for i in range(0,len(level),2)]

    def print_tree(self):
        for i , level in enumerate(self.levels):
            print("\n Level " , i)
            for j in level:
                print(j , "\t")
        

        
    def get_proof(self,trans):
        proof = []
        index = self.trans.index(trans)
        for level in self.levels[:-1]:
            is_right_node = index % 2 == 1
            sibling_index = index - 1 if is_right_node else index + 1
            proof.append({
                "hash": level[sibling_index],
                "position": "left" if is_right_node else "right"
            })
            index //= 2
        return proof 

    @staticmethod
    def verify_proof(root , trans , proof):
        current = calculate_hash(trans)
        for step in proof:
            if step["position"] == "left":
                current = calculate_hash(step["hash"] + current)
            else:
                current = calculate_hash(current + step["hash"])
        return current == root

tx = ["Hello World","Hihi","Hoho","India"]
treeeee = MerkleTree(tx)

transw = "Hello World"
ac = treeeee.get_proof(transw)
treeeee.print_tree()

trs = "LLLL"

print(treeeee.verify_proof(treeeee.root , transw ,ac ))
