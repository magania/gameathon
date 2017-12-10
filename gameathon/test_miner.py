from miner import Miner

from binascii import unhexlify

mm = Miner()
mm.init()
#mm.target_changed(b'00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
block = {'prev_block_hash': '000001906e2e03ee9d509434e8f934066749116115d13c82f0821bfeb757e70e', 'hash': '################################################################', 'height': 5, 'message': 'TeamZero Rules!', 'merkle_hash': '36c3168cf10a2baa45fc283d6bdc8c73f08f749e333d74c35f157d461b510daa', 'transactions': [{'hash': '36c3168cf10a2baa45fc283d6bdc8c73f08f749e333d74c35f157d461b510daa', 'inputs': [{'prev_hash': '0000000000000000000000000000000000000000000000000000000000000000', 'vout': -1, 'script_sig': 'TeamZero CoinBase'}], 'outputs': [{'script': 'address', 'value': 5000000000}], 'size': 0, 'confirmations': 0}], 'reward': 50, 'nonce': None, 'user': 'TeamZero Miner!', 'target': None, 'created_at': None, 'version_': '1'}
mm.mine_block(block)
