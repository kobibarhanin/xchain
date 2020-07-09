import json
import copy

from blockchain.blockchain import Blockchain
from encryption.encryption import encrypt, decrypt, sign, verify
from utils.utils import printout
from entry.entries import entries


Blockchain.get_chain = printout(Blockchain.get_chain)


def issuer_signup(_entries, key_path):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        _entry['signature'] = sign(str(_entry['listing']), key_path)
    return _tmp_entries


def encrypt_entries(_entries, enc_key):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        _entry['listing'] = encrypt(str(_entry['listing']), enc_key).decode('utf-8')
    return _tmp_entries


def issuer_verify(_entries, ver_key):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        verify(str(_entry['listing']), _entry['signature'], ver_key)
    return _tmp_entries


def decrypt_entries(_entries, dec_key):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        deced = decrypt(str(_entry['listing']), dec_key).decode('utf-8')
        deced = json.loads(deced.replace("'", "\""))
        _entry['listing'] = deced
    return _tmp_entries


if __name__ == '__main__':

    blockchain = Blockchain()
    chain = blockchain.get_chain()

    print(f'entries:\n{entries}')

    signed_entries = issuer_signup(entries)
    print(f'entries signed:\n{entries}')

    encrypted_entries = encrypt_entries(signed_entries)
    print(f'entries encrypted:\n{encrypted_entries}')

    blockchain.mine_block(encrypted_entries)
    blockchain.get_chain()
    chain_entries = blockchain.chain[1]['entries']

    decrypted_entries = decrypt_entries(chain_entries)
    print(f'entries decrypted:\n{decrypted_entries}')
    issuer_verify(decrypted_entries)
