import hashlib 
import time 

def get_hash(data : str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def mine(block_data: str , target: str):
    nonce = 0
    start_time = time.time()
    attempts = 0

    while True:
        data = block_data + str(nonce)
        block_hash = get_hash(data)
        attempts += 1

        if block_hash < target:
            end_time = time.time()
            total = end_time - start_time
            return{
                "nonce" : nonce,
                "blockhash" : block_hash,
                "attempts" : attempts,
                "total_time": total
            }
        nonce += 1

target = (
    "0fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    # "0000000fffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
)


result = mine("Bitcoin" , target)


print("Nonce:", result["nonce"])
print("BlockHash: ", result["blockhash"])
print("Total Time Taken: ", result["total_time"])
print("Target:", target)
print("attempts:", result["attempts"])