from miner import Miner
from transaction_manager import TransactionManager
import requests
import json 

_GAME = 'testnet3'
_ENDPOINT_BLOCKS = 'https://gameathon.mifiel.com/api/v1/games/{}/blocks' \
                .format(_GAME)


mm = Miner()
mm.init(1)
tm = TransactionManager()
tm.init()
response = requests.get(_ENDPOINT_BLOCKS)
blocks = json.loads(response.content)
print(blocks)
ob = blocks[-1]
print(ob)
new_block = tm.build_block(ob)
mm.mine_block(new_block)
