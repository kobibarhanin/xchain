from blockchain.blockchain import Blockchain
from entry.entry import issuer_signup, encrypt_entries, issuer_verify, decrypt_entries
from entry.entries import entries
from utils.utils import printout

from encryption.keys_config import ENC_KEY, SIG_KEY_PATH, VER_KEY_PATH


Blockchain.get_chain = printout(Blockchain.get_chain)


if __name__ == '__main__':

    blockchain = Blockchain()
    chain = blockchain.get_chain()

    print(f'entries:\n{entries}')

    signed_entries = issuer_signup(entries, SIG_KEY_PATH)
    print(f'entries signed:\n{entries}')

    encrypted_entries = encrypt_entries(signed_entries, ENC_KEY)
    print(f'entries encrypted:\n{encrypted_entries}')

    blockchain.mine_block(encrypted_entries)
    blockchain.get_chain()
    chain_entries = blockchain.chain[1]['entries']

    decrypted_entries = decrypt_entries(chain_entries, ENC_KEY)
    print(f'entries decrypted:\n{decrypted_entries}')
    issuer_verify(decrypted_entries, VER_KEY_PATH)


# from blockchain.encryption import issuer_signup
