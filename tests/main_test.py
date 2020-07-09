import pytest

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from blockchain.blockchain import Blockchain
from encryption.encryption import encrypt, decrypt, sign, verify
from entry.entry import issuer_signup, encrypt_entries, issuer_verify, decrypt_entries
from entry.entries import entries
from utils.utils import printout

from .test_keys_config import ENC_KEY, SIG_KEY_PATH, VER_KEY_PATH

from encryption.keymaker import generate_key

generate_key(f'{path.dirname(path.abspath(__file__))}/test_keys')

Blockchain.get_chain = printout(Blockchain.get_chain)


@pytest.fixture()
def setup_blockchain():
    blockchain = Blockchain()
    return blockchain


def test_base_chain(setup_blockchain):
    blockchain = setup_blockchain
    assert len(blockchain.chain) == 1


def test_mine_block(setup_blockchain):
    blockchain = setup_blockchain
    blockchain.mine_block(entries)
    assert len(blockchain.chain) == 2
    assert len(blockchain.chain[1]['entries']) == len(entries)


def test_encryption():
    plain_text = 'text to encrypt'
    encrypted = encrypt(plain_text, ENC_KEY)
    decrypted = decrypt(encrypted, ENC_KEY).decode('utf-8')
    assert plain_text == decrypted


def test_entries_encryption():
    encrypted_entries = encrypt_entries(entries, ENC_KEY)
    decrypted_entries = decrypt_entries(encrypted_entries, ENC_KEY)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']


def test_signing():
    plain_text = 'text to encrypt'
    signature = sign(plain_text, SIG_KEY_PATH)
    verify(plain_text, signature, VER_KEY_PATH)


def test_entries_signing():
    signed_entries = issuer_signup(entries, SIG_KEY_PATH)
    issuer_verify(signed_entries, VER_KEY_PATH)


def test_block_encryption(setup_blockchain):
    blockchain = setup_blockchain
    encrypted_entries = encrypt_entries(entries, ENC_KEY)
    blockchain.mine_block(encrypted_entries)
    chain_entries = blockchain.chain[1]['entries']
    decrypted_entries = decrypt_entries(chain_entries, ENC_KEY)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']


def test_block_signing(setup_blockchain):
    blockchain = setup_blockchain
    signed_entries = issuer_signup(entries, SIG_KEY_PATH)
    blockchain.mine_block(signed_entries)
    chain_entries = blockchain.chain[1]['entries']
    issuer_verify(chain_entries, VER_KEY_PATH)


def test_block_total_security(setup_blockchain):
    blockchain = setup_blockchain
    signed_entries = issuer_signup(entries, SIG_KEY_PATH)
    encrypted_entries = encrypt_entries(signed_entries, ENC_KEY)
    blockchain.mine_block(encrypted_entries)
    chain_entries = blockchain.chain[1]['entries']
    decrypted_entries = decrypt_entries(chain_entries, ENC_KEY)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']
    issuer_verify(decrypted_entries, VER_KEY_PATH)
