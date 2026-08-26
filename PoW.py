import hashlib 
import time 

def get_hash(data : str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def mine(block_data : str , target: str):
    nonce = 0
    start_time = time.time()
    attempts = 0

    while True:
        data = block_data + str(nonce)
        blockhash = get_hash(data)
        attempts += 1

        if blockhash < target:
            end_time = time.time()
            total = end_time - start_time
            return{
                "nonce" : nonce,
                "blockhash" : blockhash,
                "total" : total,
                "attempts" : attempts           
            }
        nonce += 1

target = (
    "0fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "0000000fffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
)

result = mine("Hello World" , target)

print("Nonce: " , result["nonce"])
print("BlockHash: " , result["blockhash"])
print("Total Time Taken: " , result["total"])
print("Target: " , target)
print("attempts:", result["attempts"])