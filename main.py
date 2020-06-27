import json

from blockchain.blockchain import Blockchain
from encryption.encryption import encrypt, decrypt,sign, verify
from utils.utils import printout


Blockchain.get_chain = printout(Blockchain.get_chain)


ENC_KEY = b'1234567890123456'
SIG_KEY_PATH = 'items/private_key.pem'
VER_KEY_PATH = 'items/public_key.pem'

entries = [
    {'issuer': 'haifa university', 'subject': 'student_1', 'listing': {'grade': '85', 'subject': 'intro to cs'}},
    {'issuer': 'haifa university', 'subject': 'student_1', 'listing': {'grade': '85', 'subject': 'data structures'}},
]


def issuer_signup(_entries):
    for _entry in _entries:
        _entry['signature'] = sign(str(_entry['listing']), SIG_KEY_PATH)


def encrypt_entries(_entries):
    for _entry in _entries:
        _entry['listing'] = encrypt(str(_entry['listing']), ENC_KEY).decode('utf-8')


def issuer_verify(_entries):
    for _entry in _entries:
        verify(str(_entry['listing']), _entry['signature'], VER_KEY_PATH)


def decrypt_entries(_entries):
    for _entry in _entries:
        deced = decrypt(str(_entry['listing']), ENC_KEY).decode('utf-8')
        deced = json.loads(deced.replace("'", "\""))
        _entry['listing'] = deced


if __name__ == '__main__':

    blockchain = Blockchain()
    chain = blockchain.get_chain()

    print(f'entries:\n{entries}')

    issuer_signup(entries)
    print(f'entries signed:\n{entries}')

    encrypt_entries(entries)
    print(f'entries encrypted:\n{entries}')

    blockchain.mine_block(entries)
    blockchain.get_chain()
    chain_entries = blockchain.chain[1]['entries']

    decrypt_entries(chain_entries)
    print(f'entries decrypted:\n{chain_entries}')
    issuer_verify(chain_entries)
