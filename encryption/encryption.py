import base64
from Crypto.Cipher import AES

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def encrypt(entry, key):
    msg_text = entry.ljust(64)
    cipher = AES.new(key, AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded


def decrypt(entry, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(entry))
    return decoded


def sign(text, key_path='../items/private_key.pem'):

    digest = SHA256.new()
    digest.update(text.encode())

    # Read shared key from file
    with open(key_path, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Load private key and sign message
    signer = PKCS1_v1_5.new(private_key)

    return signer.sign(digest)


def verify(text, signature, key_path='../items/public_key.pem'):

    digest = SHA256.new()
    digest.update(text.encode())

    # Load public key and verify message
    with open(key_path, "r") as myfile:
        public_key = RSA.importKey(myfile.read())
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, signature)
    assert verified, 'Signature verification failed'
    print(f'Successfully verified: {text}')


if __name__ == '__main__':

    test = 'sign me!'
    sig = sign(test, '../items/private_key.pem')
    verify(test, sig, '../items/public_key.pem')
