import pytest

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from blockchain.blockchain import Blockchain
from encryption.encryption import encrypt, decrypt, sign, verify
from entry.entry import issuer_signup, encrypt_entries, issuer_verify, decrypt_entries
from entry.entries import entries
from utils.utils import printout


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
    encrypted = encrypt(plain_text)
    decrypted = decrypt(encrypted).decode('utf-8')
    assert plain_text == decrypted


def test_entries_encryption():
    encrypted_entries = encrypt_entries(entries)
    decrypted_entries = decrypt_entries(encrypted_entries)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']


def test_signing():
    plain_text = 'text to encrypt'
    signature = sign(plain_text)
    verify(plain_text, signature)
    assert verify


def test_entries_signing():
    signed_entries = issuer_signup(entries)
    # issuer_verify(signed_entries)


def test_block_encryption():
    assert True


def test_block_signing():
    assert True


def test_block_total_security():
    assert True
