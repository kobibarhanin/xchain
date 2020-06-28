import base64
from Crypto.Cipher import AES

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


from encryption.keys_config import ENC_KEY, SIG_KEY_PATH, VER_KEY_PATH


def encrypt(entry, key=ENC_KEY):
    msg_text = entry.ljust(64)
    cipher = AES.new(key, AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded


def decrypt(entry, key=ENC_KEY):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(entry))
    return decoded.strip()


def sign(text, key_path=SIG_KEY_PATH):

    digest = SHA256.new()
    digest.update(text.encode())

    # Read shared key from file
    with open(key_path, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Load private key and sign message
    signer = PKCS1_v1_5.new(private_key)

    return signer.sign(digest)


def verify(text, signature, key_path=VER_KEY_PATH):

    digest = SHA256.new()
    digest.update(text.encode())

    # Load public key and verify message
    with open(key_path, "r") as myfile:
        public_key = RSA.importKey(myfile.read())
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, signature)
    assert verified, 'Signature verification failed'


if __name__ == '__main__':

    test = 'sign me!'
    sig = sign(test, '../items/private_key.pem')
    verify(test, sig, '../items/public_key.pem')
