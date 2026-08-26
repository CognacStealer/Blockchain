from ecdsa import SECP256k1 , SigningKey
import hashlib



sign_key = SigningKey.generate(curve=SECP256k1)
verify_key = sign_key.get_verifying_key()

private_key = sign_key.to_string().hex()
public_key = verify_key.to_string().hex()

print("Private Key:   " , private_key)
print("Public Key:    " , public_key)

def get_hash(data : str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

msg = "Hello World"
msg_hash = get_hash(msg)

print("Hashed Msg: " , msg_hash)

signature = sign_key.sign(bytes.fromhex(msg_hash))
signature_hex = signature.hex()

try:
    is_valid = verify_key.verify(bytes.fromhex(signature_hex) , bytes.fromhex(msg_hash))
    print("This a good signature")
except Exception:
    print("This is fake signature")

fake_msg = "Helloooo"
fake_hash = get_hash(fake_msg)

try:
    is_valid = verify_key.verify(bytes.fromhex(signature_hex) , bytes.fromhex(fake_hash))
    print("This a good signature")
except Exception:
    print("This is fake signature")





