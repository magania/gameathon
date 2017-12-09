from miner import Miner

from binascii import unhexlify

mm = Miner()
#mm.target_changed(b'00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
block = {'version': b'1',
         'prev_block_hash': b'dcc7d4fd08cbc0484f3f2eda3cc20f2b2d1b4e5eebfaafc82d5526d73637ff49',
         'merkle_hash': b'dcc7d4fd08cbc0484f3f2eda3cc20f2b2d1b4e5eebfaafc82d5526d73637ff49',
         'message': b'test message',
         'transactions': []}
mm.mine_block(block)
